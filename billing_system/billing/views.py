import threading
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Bill, BillItem, Denomination, Product

ROUND = lambda x: x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def send_invoice_email_async(subject, html_body, to_email):
    def _send():
        email = EmailMessage(subject=subject, body=html_body, to=[to_email])
        email.content_subtype = "html"
        email.send(fail_silently=False)

    thread = threading.Thread(target=_send, daemon=True)
    thread.start()


def compute_change_distribution(change_amount: Decimal, denominations_qs):
    """
    Greedy algorithm but respects available counts. Returns (distribution, remainder).
    distribution: dict {value_str: count_to_give}
    remainder: Decimal amount that couldn't be dispensed due to shortages
    """
    remaining = change_amount
    distribution = {}
    for denom in denominations_qs:
        if remaining <= 0:
            distribution[str(denom.value)] = 0
            continue
        value = denom.value
        max_need = int((remaining // value))
        give = min(max_need, denom.count)
        distribution[str(value)] = give
        remaining -= Decimal(give) * value
        remaining = ROUND(remaining)
    # print(distribution, remaining)
    return distribution, remaining  # remainder in decimal


@require_http_methods(["GET", "POST"])
@csrf_exempt
def billing_page(request):
    if request.method == "GET":
        products = Product.objects.all()
        denominations = Denomination.objects.all()
        return render(
            request,
            "billing/billing_page.html",
            {"products": products, "denominations": denominations},
        )

    # POST: process billing
    data = request.POST
    customer_email = data.get("customer_email")
    paid_amount = Decimal(data.get("paid_amount", "0"))
    # Items: expect product_id[] and qty[]
    product_ids = request.POST.getlist("product_id[]")
    quantities = request.POST.getlist("quantity[]")

    denominations = Denomination.objects.all().order_by(
        "-value"
    )  # denom counts from the form as denomination_<value>

    items = []
    total_before_tax = Decimal("0.00")
    total_tax = Decimal("0.00")
    print("PRODUCT IDS RECEIVED:", product_ids)
    with transaction.atomic():
        # lock or check stocks
        for pid, qty in zip(product_ids, quantities):
            qty_i = int(qty)
            try:
                p = Product.objects.select_for_update().get(product_id=pid)
            except Product.DoesNotExist:
                return render(
                    request,
                    "billing/billing_page.html",
                    {
                        "error": f"Product {pid} not found",
                        "products": Product.objects.all(),
                        "denominations": denominations,
                    },
                )
            if p.stock < qty_i:
                return render(
                    request,
                    "billing/billing_page.html",
                    {
                        "error": f"Insufficient stock for {p.product_id} ({p.stock} available)",
                        "products": Product.objects.all(),
                        "denominations": denominations,
                    },
                )
            # compute line
            unit_price = p.unit_price
            purchase_price = p.purchase_price
            unit = p.unit_price if int(purchase_price) <= 0 else purchase_price
            tax_amt_item = unit * Decimal(p.tax_percent) / Decimal("100.00")
            tax = tax_amt_item * qty_i
            line_total = (unit * qty_i) + tax
            items.append(
                {
                    "product": p,
                    "quantity": qty_i,
                    "unit_price": unit_price,
                    "purchase_price": purchase_price,
                    "tax_percent": p.tax_percent,
                    "tax_amt_item": tax_amt_item,
                    "line_total": ROUND(line_total),
                }
            )
            total_before_tax += unit * qty_i
            total_tax += tax
            # reduce stock
            p.stock -= qty_i
            p.save()

        total_before_tax = ROUND(total_before_tax)
        total_tax = ROUND(total_tax)
        total_amount = ROUND(total_before_tax + total_tax)
        change_amount = (
            (paid_amount - total_amount)
            if paid_amount >= total_amount
            else Decimal("0.00")
        )

        # calculate denominations for change using current shop denominations
        dist, remainder = compute_change_distribution(change_amount, denominations)
        # if remainder != 0, then,return exact change
        # Update Denomination counts only when change is being given
        # reduce available counts for change given:
        for denom in denominations:
            val_str = str(denom.value)
            give = dist.get(val_str, 0)
            if give:
                denom.count = denom.count - give
                denom.save()

        # create Bill and BillItems
        bill = Bill.objects.create(
            customer_email=customer_email,
            total_before_tax=total_before_tax,
            total_tax=total_tax,
            total_amount=total_amount,
            paid_amount=paid_amount,
            change_amount=change_amount - remainder,
            change_denominations=dist,
            metadata={"change_remainder_unable_to_dispense": str(remainder)},
        )

        for it in items:
            BillItem.objects.create(
                bill=bill,
                product=it["product"],
                quantity=it["quantity"],
                unit_price=it["unit_price"],
                purchase_price=it["purchase_price"],
                tax_percent=it["tax_percent"],
                tax_amt_item=it["tax_amt_item"],
                line_total=it["line_total"],
            )

    # render invoice page and send email asynchronously
    html_body = render_to_string(
        "billing/invoice.html",
        {
            "bill": bill,
        },
    )
    send_invoice_email_async(
        subject=f"Invoice #{bill.pk}", html_body=html_body, to_email=customer_email
    )

    return render(request, "billing/invoice.html", {"bill": bill, "sent_email": True})


def customer_purchases(request):
    email = request.GET.get("email")
    bills = (
        Bill.objects.filter(customer_email=email).order_by("-created_at")
        if email
        else []
    )
    return render(
        request, "billing/purchase_list.html", {"bills": bills, "email": email}
    )


def purchase_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, "billing/purchase_detail.html", {"bill": bill})
