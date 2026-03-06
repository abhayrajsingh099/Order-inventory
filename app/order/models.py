from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(stock__gte=0),
            name="stock_gte_0"),
            models.CheckConstraint(condition=models.Q(price__gte=0),
            name="price_gte_0"),
        ]

    def __str__(self):
        return self.name


class OrderStatus(models.TextChoices):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING_PAYMENT"
    PAID = "PAID"
    FAILED = "FAILED"

class Order(models.Model):
    user_id = models.CharField(max_length=255, blank=False ,null=False)
    status = models.CharField(max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # idempotency_key = models.CharField(max_length=255, unique=True, blank=False, null=False)

    class Meta:
        indexes  = [
            models.Index(fields=["user_id", "-created_at"], name='index_user_id_created_at')
        ]

    def __str__(self):
        return f"{self.user_id}--{self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product")
    quantity = models.IntegerField(null=False)
    price_at_purchase = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gte=1),
            name="quantity_gte_1"),
            models.CheckConstraint(condition=models.Q(price_at_purchase__gte=0),
            name="price_at_purchase_gte_0"),
            models.UniqueConstraint(fields=["order", "product"],
            name="unique_order_product"),
        ]

        indexes  = [
            models.Index(fields=["order"], name='index_order')
        ]

    def __str__(self):
        return f"{self.order_id}-{self.product_id}-{self.quantity}"


"""
Outbox model gets task that needs to be completed by an external-side-effect-api
but async. and guarantees a task will be done.
"""
# PENDING
# PROCESSING
# DONE
# FAILED
class OutboxEvent(models.Model):
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    status = models.CharField(max_length=50, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    attempt_count = models.IntegerField(default=0)
    locked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.event_type}-{self.status}"