from recharge.serializers import DepositWalletSerializer, DepositTransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class InitiateTransactionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepositWalletSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CreateDepositTransactionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepositTransactionSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
