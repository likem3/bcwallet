from drf_yasg import openapi
from account.serializers import WalletSerializer
from bcwallet.settings import HELPER_TEXT, BLOCKCHAIN_OPTIONS
from rest_framework import status

create_wallet_schema = {
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["user_id", "blockchain"],
        properties={
            "user_id": openapi.Schema(
                type=openapi.TYPE_INTEGER, description=HELPER_TEXT["user_id"]
            ),
            "blockchain": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=list(dict(BLOCKCHAIN_OPTIONS).keys()),
                description=HELPER_TEXT["blockchain"],
            ),
        },
    ),
    "responses": {
        status.HTTP_201_CREATED: openapi.Response(
            description="Success created wallet", schema=WalletSerializer
        ),
        status.HTTP_200_OK: openapi.Response(
            description="Success get wallet data", schema=WalletSerializer
        ),
    },
}

get_account_list_schema = {
    "manual_parameters": [
        openapi.Parameter(
            name="search",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Search in user_id, email, or username.",
        ),
        openapi.Parameter(
            name="ordering",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='Specify the ordering of the results. Prefix with "-" for \
                descen ding order. Available fields: id, created_at, user_id.',
        ),
        openapi.Parameter(
            name="page",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="The page number of the results.",
        ),
        openapi.Parameter(
            name="size",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="The number of items to return per page.",
        ),
    ]
}
