from django.utils import timezone
from .models import OutboxEvent, Order
from datetime import timedelta
from django.db.models import F


VISIBILITY_TIMEOUT = 30  # seconds
MAX_ATTEMPT = 5

def process_outbox():

    cutoff = timezone.now() - timedelta(seconds=VISIBILITY_TIMEOUT)

    events = OutboxEvent.objects.filter(
        status="PENDING"
        ) | OutboxEvent.objects.filter(
            status="PROCESSING", locked_at__lt=cutoff
        )


    for event in events:

        # 1. Atomic Updation, avoid race
        updated = OutboxEvent.objects.filter(
            id=event.id,
            status__in=["PENDING", "PROCESSING"]
        ).update(
            status="PROCESSING",
            attempt_count=F("attempt_count")+1,
            locked_at = timezone.now()
        )

        if updated == 0:
            continue

        if event.attempt_count >= MAX_ATTEMPT:
            event.status = "FAILED"
            event.save()
            continue

        # 2. side - effect execution
        order_id = event.payload["order_id"]

        order = Order.objects.get(id=order_id)

        try:
            success = charge_payment(order.id) #idempotent call, simulation

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
    return random.random() < 0.4

