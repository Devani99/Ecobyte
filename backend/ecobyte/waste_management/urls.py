from django.urls import path
from .views import classify_waste, CustomAuthToken, register_user

urlpatterns = [
    path('classify/', classify_waste, name='classify-waste'),
    path('auth/login/', CustomAuthToken.as_view(), name='auth-login'),
    path('auth/register/', register_user, name='auth-register'),
]
