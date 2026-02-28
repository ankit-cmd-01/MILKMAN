"""Seed command for demo users and dairy products."""

from django.core.management.base import BaseCommand

from products.models import Category, Product
from users.models import User


class Command(BaseCommand):
    help = "Create default MilkMan users and sample dairy products."

    def handle(self, *args, **options):
        admin_email = "ankits@gmail.com"
        admin_password = "ankit@123"
        customer_email = "customer1@test.com"
        customer_password = "strongpassword123"

        admin_user, admin_created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                "is_superuser": True,
                "is_staff": True,
                "role": User.Roles.ADMIN,
                "first_name": "Ankit",
                "last_name": "Admin",
            },
        )
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.role = User.Roles.ADMIN
        admin_user.set_password(admin_password)
        admin_user.save()

        customer_user, customer_created = User.objects.get_or_create(
            email=customer_email,
            defaults={
                "role": User.Roles.CUSTOMER,
                "first_name": "Customer",
                "last_name": "One",
                "phone_number": "9999999999",
                "address": "Mumbai, Maharashtra",
            },
        )
        customer_user.role = User.Roles.CUSTOMER
        customer_user.set_password(customer_password)
        customer_user.save()

        milk_category, _ = Category.objects.get_or_create(
            name="Milk & Beverages",
            defaults={"description": "Fresh milk and drinkables"},
        )
        dairy_category, _ = Category.objects.get_or_create(
            name="Dairy Essentials",
            defaults={"description": "Butter, paneer, curd and ghee"},
        )

        sample_products = [
            {
                "category": milk_category,
                "name": "Amul Milk",
                "description": "Toned milk for daily use",
                "price": "64.00",
                "stock_quantity": 300,
                "unit": "litre",
                "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/Amul.svg/512px-Amul.svg.png",
            },
            {
                "category": dairy_category,
                "name": "Amul Butter",
                "description": "Salted table butter",
                "price": "58.00",
                "stock_quantity": 160,
                "unit": "pack",
                "image_url": "https://images.unsplash.com/photo-1473448912268-2022ce9509d8",
            },
            {
                "category": dairy_category,
                "name": "Amul Paneer",
                "description": "Fresh paneer block",
                "price": "92.00",
                "stock_quantity": 120,
                "unit": "pack",
                "image_url": "https://images.unsplash.com/photo-1589881133825-bbb7d1fa7f0b",
            },
            {
                "category": dairy_category,
                "name": "Mother Dairy Curd",
                "description": "Creamy plain curd",
                "price": "42.00",
                "stock_quantity": 220,
                "unit": "pack",
                "image_url": "https://images.unsplash.com/photo-1571212515416-fca88cbf3a5a",
            },
            {
                "category": dairy_category,
                "name": "Ghee (Amul)",
                "description": "Pure cow ghee",
                "price": "620.00",
                "stock_quantity": 65,
                "unit": "kg",
                "image_url": "https://images.unsplash.com/photo-1627483262769-8bc9f8af95b7",
            },
            {
                "category": dairy_category,
                "name": "Chitale Shrikhand",
                "description": "Traditional shrikhand",
                "price": "110.00",
                "stock_quantity": 80,
                "unit": "pack",
                "image_url": "https://images.unsplash.com/photo-1596797038530-2c107229654b",
            },
            {
                "category": milk_category,
                "name": "Lassi",
                "description": "Sweet lassi bottle",
                "price": "30.00",
                "stock_quantity": 140,
                "unit": "pack",
                "image_url": "https://images.unsplash.com/photo-1626074353765-517a681e40be",
            },
            {
                "category": milk_category,
                "name": "Buttermilk",
                "description": "Masala chaas",
                "price": "22.00",
                "stock_quantity": 180,
                "unit": "pack",
                "image_url": "https://images.unsplash.com/photo-1551024709-8f23befc6cf7",
            },
        ]

        for data in sample_products:
            Product.objects.update_or_create(
                name=data["name"],
                defaults=data,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completed. admin_created={admin_created}, customer_created={customer_created}"
            )
        )
