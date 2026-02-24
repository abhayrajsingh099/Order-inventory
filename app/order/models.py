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

class Order(models.Model):
    user_id = models.CharField(max_length=255, blank=False ,null=False)
    product_id = models.IntegerField(blank=False, null=False)
    status = models.CharField(max_length=50, default="CREATED")

    def __str__(self):
        return f"{self.user_id}--{self.product_id}"