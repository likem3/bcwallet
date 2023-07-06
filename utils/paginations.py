from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SizePagePagination(PageNumberPagination):
    page_size_query_param = "size"

    def get_paginated_response(self, data):
        return Response(
            {
                "size": self.page.paginator.per_page,
                "page": self.page.number,
                "total": self.page.paginator.count,
                "results": data,
            }
        )
