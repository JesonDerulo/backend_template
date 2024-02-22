# api/views.py

from typing import Any, Dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializerWithToken, UserSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# imports for User Login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from api.serializers import UserSerializerWithToken


@api_view(["POST"])
def register_user(request):
    data = request.data
    try:
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Check if user enter all requied info 
        if not username or not email or not password:
            message = {
                "detail": "Please provide all required fields: username, email, and password"
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user with the given email already exists
        if User.objects.filter(email=email).exists():
            message = {"detail": "User with this email already exists!!"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        # create a new User with valid user info
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except IntegrityError as e:
        # Handle any other integrity error, if needed
        message = {"detail": "Error creating user"}
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    try:
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except ValidationError as e:
        return Response(
            {"detail": "Error in serialization", "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
