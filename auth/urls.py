from django.urls import path
from auth.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path("", CustomTokenObtainPairView.as_view(), name="token-create"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
]
