from drf_yasg import generators, openapi
from drf_yasg.views import get_schema_view
from django.conf import settings as app_settings


class BothHttpAndHttpsSchemaGenerator(generators.OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        if app_settings.ENVIRONMENT_SETTING == "local":
            schema.schemes = ["http"]
        else:
            schema.schemes = ["https"]

        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="bcwallet API",
        description="Krypto wallet api for client",
        default_version="v0.0001",
        license=openapi.License(name="MIT"),
        terms_of_service="https://github.com/likem3/bcwallet/",
        contact=openapi.Contact(email="islike1221@gmail.com"),
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
)
