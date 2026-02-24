from django.db import transaction
from django.db import IntegrityError
from .models import Product, Order
from django.db.models import F


def make_order(p_id:int, data:dict) -> Order:

    with transaction.atomic():
        try:
            # m-1 select_for_update() can be used as well
            # m-2 one-line direct sql execution
            Product.objects.filter(id=p_id).update(
                stock=F('stock') - 1
            )
            order = Order.objects.create(**data)
        except IntegrityError:
            return None

    return order


