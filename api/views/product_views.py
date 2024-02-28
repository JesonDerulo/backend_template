from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Product
from rest_framework import status
from api.serializers import ProductSerializer
from django.core.exceptions import ObjectDoesNotExist


@api_view(["GET"])
def get_products(request):
    try:
        products = Product.objects.all()
        if not products:
            return Response(
                {"detail": "No products found"}, status=status.HTTP_204_NO_CONTENT
            )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_product(request, pk):

    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response(
            {"detail": "No product found!!!"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
