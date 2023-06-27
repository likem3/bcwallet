from recharge.serializers import DepositWalletSerializer
# from account.models import Account
# from django.shortcuts import get_object_or_404
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema


class InitiateTransactionView(generics.CreateAPIView):
    serializer_class = DepositWalletSerializer

    @swagger_auto_schema(
        auto_query_parameter=False  # Disable querying the account parameter
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     account = get_object_or_404(Account, user_id=self.kwargs.get("user_id"))
    #     context["account"] = account
    #     return context
