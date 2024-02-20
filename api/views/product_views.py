from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Product
from rest_framework import status
from api.serializers import ProductSerializer


@api_view(['GET'])
def get_products(request):
    try:
        products = Product.objects.all()
        if not products:
            return Response({'message': 'No products found'}, status=status.HTTP_204_NO_CONTENT)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)