from django.utils import timezone
from .models import OutboxEvent, Order

def process_outbox():

    events = OutboxEvent.objects.filter(status="PENDING")

    for event in events:

        # 1. Atomic Updation, avoid race
        updated = OutboxEvent.objects.filter(
            id=event.id,
            status="PENDING"
        ).update(status="PROCESSING")

        if updated == 0:
            continue

        # 2. side - effect execution
        order_id = event.payload["order_id"]

        order = Order.objects.get(id=order_id)

        try:
            success = charge_payment(order.id) #idempotent call

            if success:
                order.status = "PAID"
                event.status = "DONE"
            else:
                order.status = "FAILED"
                event.status = "FAILED"

            order.save()
            event.processed_at = timezone.now()
            event.save()

        except Exception:
            event.status = "FAILED"
            event.save()


import random
import time

def charge_payment(order_id):
    # simulate network delay
    time.sleep(1)

    # simulate success 80% of time
    return random.random() < 0.3

