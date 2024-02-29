from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.models import Product, Review
from rest_framework import status
from api.serializers import ProductSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated



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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_review(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    data = request.data 

    # 1 - check if user already reviewed the product
    already_exists = product.review_set.filter(user=user).exists()
    if already_exists:
        content = {'detail' : "Product already reviewed"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # 2 - No Rating or 0 
    elif data['rating'] == 0:
        content = {'detail' : "Please select a rating!"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.username,
            rating=data['rating'],
            comment=data['comment']
        )
        
        # 3 - caculate the averge rating for the product
        # get the count of total reviews
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        # sum all ratings
        total = 0 
        for i in reviews:
            total += i.rating

        product.rating = total / len(reviews)
        product.save()

        return Response('Review Added')