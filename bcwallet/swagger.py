from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="bcwallet API",
        description="Krypto wallet api for client",
        default_version="v0.0001",
        license=openapi.License(name="MIT"),
        terms_of_service="https://github.com/likem3/bcwallet/",
        contact=openapi.Contact(email='islike1221@gmail.com'),
    ),
    public=True,
)