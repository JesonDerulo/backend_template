from django.urls import path
from api.views import user_views as views

urlpatterns = [
    path("register/", views.register_user, name="register-user"),
    # Check the MyTokenObtainPairView not TokenObtainPairView
    path("login/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("profile/", views.get_user_profile, name="user-profile"),
    path("profile/update/", views.update_user_profile, name='update-user-profile'),
]
