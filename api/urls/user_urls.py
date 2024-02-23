from django.urls import path
from api.views import user_views as views

urlpatterns = [
    path("register/", views.register_user, name="register-user"),
    # Check the MyTokenObtainPairView not TokenObtainPairView
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("profile/", views.getUserProfile, name="user-profile"),
]
