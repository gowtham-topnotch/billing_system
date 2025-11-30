from django import forms


class BillingItemForm(forms.Form):
    product_id = forms.CharField(max_length=100)
    quantity = forms.IntegerField(min_value=1)


class BillingForm(forms.Form):
    customer_email = (
        forms.EmailField()
    )  # To handle dynamic list of items in js and post arrays product_id[], quantity[]
    paid_amount = forms.DecimalField(decimal_places=2, max_digits=12)
