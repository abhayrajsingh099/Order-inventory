from django.contrib import admin
from .models import Product, Order, OutboxEvent, OrderItem



admin.site.register(Product)
# admin.site.register(Order)
admin.site.register(OutboxEvent)
admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

