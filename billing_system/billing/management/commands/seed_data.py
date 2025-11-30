from billing.models import Denomination, Product
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed sample products and denominations"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Denomination.objects.all().delete()

        products = [
            {
                "product_id": "P001",
                "name": "Paracetamol 500mg",
                "stock": 50,
                "unit_price": "20.00",
                "purchase_price": "15.00",
                "tax_percent": "5.0",
            },
            {
                "product_id": "P002",
                "name": "Cough Syrup",
                "stock": 20,
                "unit_price": "150.00",
                "purchase_price": "110.00",
                "tax_percent": "12.0",
            },
            {
                "product_id": "P003",
                "name": "Vitamin C 1000mg",
                "stock": 30,
                "unit_price": "120.00",
                "purchase_price": "90.00",
                "tax_percent": "5.0",
            },
            {
                "product_id": "P004",
                "name": "Ibuprofen 200mg",
                "stock": 40,
                "unit_price": "35.00",
                "purchase_price": "25.00",
                "tax_percent": "5.0",
            },
            {
                "product_id": "P005",
                "name": "Amoxicillin 500mg",
                "stock": 25,
                "unit_price": "80.00",
                "purchase_price": "65.00",
                "tax_percent": "12.0",
            },
            {
                "product_id": "P006",
                "name": "Antiseptic Liquid 100ml",
                "stock": 18,
                "unit_price": "45.00",
                "purchase_price": "32.00",
                "tax_percent": "12.0",
            },
            {
                "product_id": "P007",
                "name": "Digital Thermometer",
                "stock": 15,
                "unit_price": "250.00",
                "purchase_price": "190.00",
                "tax_percent": "18.0",
            },
            {
                "product_id": "P008",
                "name": "Glucometer Strips (Pack of 50)",
                "stock": 10,
                "unit_price": "600.00",
                "purchase_price": "480.00",
                "tax_percent": "18.0",
            },
            {
                "product_id": "P009",
                "name": " ORS Hydration Powder",
                "stock": 60,
                "unit_price": "25.00",
                "purchase_price": "18.00",
                "tax_percent": "5.0",
            },
            {
                "product_id": "P010",
                "name": "Hand Sanitizer 100ml",
                "stock": 35,
                "unit_price": "40.00",
                "purchase_price": "28.00",
                "tax_percent": "12.0",
            },
        ]

        for p in products:
            Product.objects.create(**p)

        denoms = [
            {"value": "2000.00", "count": 2},
            {"value": "500.00", "count": 5},
            {"value": "200.00", "count": 10},
            {"value": "100.00", "count": 20},
            {"value": "50.00", "count": 50},
            {"value": "20.00", "count": 100},
            {"value": "10.00", "count": 100},
            {"value": "5.00", "count": 200},
            {"value": "2.00", "count": 200},
            {"value": "1.00", "count": 500},
        ]
        for d in denoms:
            Denomination.objects.create(**d)

        self.stdout.write(self.style.SUCCESS("Seeded products and denominations"))
