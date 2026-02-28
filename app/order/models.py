from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    stock = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(stock__gte=0),
            name="stock_gte_0"),
        ]

    def __str__(self):
        return self.name

# CREATED
# PROCESSING_PAYMENT
# PAID
# FAILED
class Order(models.Model):
    user_id = models.CharField(max_length=255, blank=False ,null=False)
    product_id = models.IntegerField(blank=False, null=False)
    status = models.CharField(max_length=50, default="CREATED")
    idempotency_key = models.CharField(max_length=255, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.user_id}--{self.product_id}"


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