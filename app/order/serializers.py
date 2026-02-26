from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['user_id', 'product_id', 'idempotency_key']
        extra_kwargs = {
            'idempotency_key': {'validators': []},
        }