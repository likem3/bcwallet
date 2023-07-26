# write schema docs here
from drf_yasg import openapi
from rest_framework import status

from django.conf import settings as app_settings
from recharge.serializers import DepositTransactionSerializer

create_ceposit_schema = {
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["merchant_code", "user_id", "currency_id", "amount"],
        properties={
            "merchant_code": openapi.Schema(
                type=openapi.TYPE_INTEGER, description=app_settings.HELPER_TEXT["merchant_code"]
            ),
            "user_id": openapi.Schema(
                type=openapi.TYPE_INTEGER, description=app_settings.HELPER_TEXT["user_id"]
            ),
            "currency_id": openapi.Schema(
                type=openapi.TYPE_INTEGER, description=app_settings.HELPER_TEXT["currency_id"]
            ),
            "amount": openapi.Schema(
                type=openapi.TYPE_NUMBER, description=app_settings.HELPER_TEXT["trx_amount"]
            ),
            "callback_url": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=app_settings.HELPER_TEXT["trx_callback_url"],
            ),
            "origin_code": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=app_settings.HELPER_TEXT["trx_origin_code"],
            ),
        },
    ),
    "responses": {
        status.HTTP_201_CREATED: openapi.Response(
            description="Success created wallet", schema=DepositTransactionSerializer
        ),
    },
}
