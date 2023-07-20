from django.contrib import admin
from django.urls import path, include
from bcwallet.swagger import schema_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("jet/", include("jet.urls", "jet")),
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path("admin/", admin.site.urls),
    path("auth/", include("auth.urls")),
    path("", include("account.urls")),
    path("", include("recharge.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
