from django.urls import path

from . import views

app_name = "billing"

urlpatterns = [
    path("", views.billing_page, name="billing_page"),
    path("purchases/", views.customer_purchases, name="purchases"),
    path("purchase/<int:bill_id>/", views.purchase_detail, name="purchase_detail"),
]
