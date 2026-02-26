from django.db import transaction
from django.db import IntegrityError
from .models import Product, Order
from django.db.models import F
from django.shortcuts import get_object_or_404



def make_order(p_id:int, data:dict) -> Order:

    try:
        with transaction.atomic():
            updated = Product.objects.filter(
                id=p_id,
                stock__gt=0
            ).update(stock=F('stock') - 1) # race condition safe

            if updated == 0:
                return None

            order = Order.objects.create(**data)
        return order

    except IntegrityError:
        return Order.objects.get(
            idempotency_key=data['idempotency_key']
        )



