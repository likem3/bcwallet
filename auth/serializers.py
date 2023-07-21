from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Customize token claims if needed
        # token['claim_name'] = 'claim_value'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Customize the token response format
        custom_response = {
            "code": 200,
            "status": True,
            "data": {
                "access_token": data["access"],
                "refresh_token": data["refresh"],
            },
        }

        return custom_response


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])
        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

        # Customize the token response format
        custom_response = {
            "code": 200,
            "status": True,
            "data": data,
        }

        return custom_response
