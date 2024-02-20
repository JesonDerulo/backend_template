from django.urls import path
from api.views import user_views as views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('login/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
]