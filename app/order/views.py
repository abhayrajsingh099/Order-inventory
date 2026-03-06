import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Prefetch, Sum, F
from django.shortcuts import get_list_or_404

from .utils import make_order
from .models import Order, OrderItem, Product
from .serializers import OrderSerializer


from django.http import JsonResponse

@api_view(['GET', 'POST'])
def create_order(request):

    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            p_id = serializer.validated_data.get('product_id')
            order = make_order(p_id, serializer.validated_data)
            if not order:
                return Response({"status":"Order creation failed"}, status=400)

            return Response(OrderSerializer(order).data, status=200)
        else:
            return Response(serializer.errors, status=400)

    return Response({'status':'View Working'}, status=200)

@api_view(['GET'])
def list_user_order(request, id):

    #Pagination
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 20))
    offset = (page - 1) * page_size



    orders = (
        Order.objects
        .filter(user_id=id)
        .order_by("-created_at")
        .prefetch_related(
        Prefetch(
            "items",
            queryset=OrderItem.objects.select_related("product")
        )
    ))[offset:offset + page_size]

    print(
        Order.objects
        .filter(user_id=id)
        .order_by("-created_at")[offset:offset + page_size]
        .explain()
    )



    response = []
    for order in orders:
        item = {}
        total_amount = 0
        item["order_id"] = order.id
        item["status"] = order.status
        items = []
        for order_item in order.items.all():
            item_detail = {}
            item_detail["product_name"] = order_item.product.name
            item_detail["quantity"] = order_item.quantity
            item_detail["price"] = order_item.price_at_purchase

            total_amount += (item_detail["quantity"] * item_detail["price"])

            items.append(item_detail)

        item["items"] = items
        item["total"] = total_amount

        response.append(item)

    data = {f'user_data-{id}':response}
    return JsonResponse(data)










