from recharge.serializers import (
    DepositWalletSerializer,
    DepositTransactionSerializer,
    UpdateReceiptTransactionSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from recharge.models import Transaction


class InitiateTransactionView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DepositWalletSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CreateDepositTransactionView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DepositTransactionSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TransactionListByUserIDView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.filter(account__status="active")
    serializer_class = DepositTransactionSerializer
    lookup_field = "account__user_id"


class TransactionDetailByUserIDView(generics.RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.filter(account__status="active")
    serializer_class = UpdateReceiptTransactionSerializer
    lookup_field = "code"

    def get_queryset(self):
        if self.request.method in ["PUT", "PATCH"]:
            query_filter = {"status": "pending"}
        else:
            query_filter = {}

        return super().get_queryset().filter(**query_filter)
