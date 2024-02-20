from django.urls import path
from api.views import user_views as views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
]