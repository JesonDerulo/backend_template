from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


from api.models import Product, Order, OrderItem
from api.serializers import ProductSerializer, OrderSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user 
    data = request.data 

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail' : 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # (1) Create a new order
        order = Order.objects.create(
            user=user,
            totalPrice=data['totalPrice']
        )

        # (2) Create order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(id=i['id'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name, 
                price=i['price']
            )
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)        