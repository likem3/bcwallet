from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.addrbank.currency import Currency
from recharge.models import Transaction
from recharge.schemas import create_ceposit_schema
from recharge.serializers import (
    CurrencySerializer,
    DepositTransactionSerializer,
    UpdateDepositTransactionSerializer
)
from utils.paginations import SizePagePagination


class CreateDepositTransactionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.filter(type="deposit", account__status="active")
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

    @swagger_auto_schema(**create_ceposit_schema)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DetailUpdateDepostiTransactionView(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.filter(type="deposit", account__status="active")
    serializer_class = UpdateDepositTransactionSerializer
    lookup_field = "code"
    allowed_methods = ["GET", "PUT"]


class DetailUpdateDepostiTransactionOriginCodeView(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.filter(type="deposit", account__status="active")
    serializer_class = UpdateDepositTransactionSerializer
    lookup_field = "origin_code"
    allowed_methods = ["GET", "PUT"]


class CurrencyListClass(APIView):
    def get(self, request):
        currency = Currency()
        curencies = currency.get_currencies()
        try:
            serializer = CurrencySerializer(data=curencies, many=True)
            serializer.is_valid()

            return Response(serializer.data, status=200)

        except Exception as e:
            print(str(e))
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
