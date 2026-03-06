from django.core.management.base import BaseCommand
from order.models import Order, OrderItem, Product
import random


class Command(BaseCommand):
    help = "Generate test orders"

    def handle(self, *args, **kwargs):
        users = [i for i in range(1001, 1010)]
        products = list(Product.objects.all())

        for _ in range(10000):
            user = random.choice(users)
            order = Order.objects.create(user_id=user, status="Created")

            selected_products = random.sample(
                products,
                k=random.randint(1, min(4, len(products)))
            )

            for product in selected_products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 5),
                    price_at_purchase=product.price,
                )

        self.stdout.write(self.style.SUCCESS("Test orders created"))