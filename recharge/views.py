from recharge.serializers import (
    DepositTransactionSerializer,
    UpdateReceiptTransactionSerializer,
    CurrencySerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from recharge.models import Transaction
from account.views import WalletListCreateView
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from utils.paginations import SizePagePagination
from apis.addrbank.currency import Currency
from rest_framework.response import Response


class DepositRechargeView(WalletListCreateView):
    allowed_methods = ["POST"]


class CreateDepositTransactionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.filter(account__status="active")
    serializer_class = DepositTransactionSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["code", "status", "type"]
    search_fields = ["code", "status", "type"]
    ordering_fields = ["id", "-id", "created_at", "-created_at"]
    pagination_class = SizePagePagination

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TransactionListByUserIDView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.filter(account__status="active")
    serializer_class = DepositTransactionSerializer
    lookup_field = "account__user_id"


class TransactionDetailByUserIDView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.filter(account__status="active")
    serializer_class = UpdateReceiptTransactionSerializer
    lookup_field = "code"

    def get_queryset(self):
        if self.request.method in ["PUT", "PATCH"]:
            query_filter = {"status": "pending"}
        else:
            query_filter = {}

        return super().get_queryset().filter(**query_filter)

    @swagger_auto_schema(operation_id="user-transaction-detail")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CurrencyListClass(APIView):

    def get(self, request):
        currency = Currency()
        curencies = currency.get_currencies()
        try:
            serializer = CurrencySerializer(data=[curencies], many=True)
            serializer.is_valid()

            return Response(serializer.data, status=200)
        
        except Exception as e:
            print(str(e))
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)