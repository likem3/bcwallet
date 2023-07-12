from recharge.serializers import (
    DepositTransactionSerializer,
    CurrencySerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from recharge.models import Transaction
from django_filters.rest_framework import DjangoFilterBackend
from utils.paginations import SizePagePagination
from apis.addrbank.currency import Currency
from rest_framework.response import Response


class CreateDepositTransactionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.filter(type="deposit", account__status="active")
    serializer_class = DepositTransactionSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["code", "user_id", "status", "type"]
    search_fields = ["code", "user_id", "status", "type"]
    ordering_fields = ["id", "-id", "created_at", "-created_at"]
    pagination_class = SizePagePagination

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TransactionListByUserIDView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.filter(account__status="active")
    serializer_class = DepositTransactionSerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        queryset = super(TransactionListByUserIDView, self).get_queryset()
        return queryset.filter(account__user_id=user_id)


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
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)