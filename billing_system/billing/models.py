from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    product_id = models.CharField(max_length=100, unique=True)
    stock = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_id} - {self.name}"


class Denomination(models.Model):
    """
    Represents shop cash denominations and how many of each are currently available.
    value: integer or decimal (we'll treat rupee integer or maybe 0.50 for coins)
    count: how many notes/coins available in shop
    """

    value = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-value"]  # largest first

    def __str__(self):
        return f"{self.value} x {self.count}"


class Bill(models.Model):
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_before_tax = models.DecimalField(max_digits=12, decimal_places=2)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    change_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    change_denominations = models.JSONField(
        null=True, blank=True
    )  # { "2000": 1, "500": 0, ... }
    metadata = models.JSONField(null=True, blank=True)  # any extra data info

    def __str__(self):
        return f"Bill #{self.pk} for {self.customer_email} at {self.created_at}"


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2)
    tax_amt_item = models.DecimalField(max_digits=5, decimal_places=2)
    line_total = models.DecimalField(
        max_digits=12, decimal_places=2
    )  # full total including tax

    def __str__(self):
        return f"{self.product} x{self.quantity}"
