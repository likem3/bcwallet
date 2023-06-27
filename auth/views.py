from rest_framework_simplejwt.views import TokenObtainPairView
from auth.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer
)
from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer