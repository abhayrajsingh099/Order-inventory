import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import make_order
from .models import Product
from .serializers import OrderSerializer

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



