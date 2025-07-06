# utils/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomProductPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # let user control how many per page

    def get_paginated_response(self, data):
        return Response({
            'total_itmes': self.page.paginator.count,  # total products matching filters
            'page': self.page.number,                     # current page number
            'page_size': self.page.paginator.per_page,    # page size
            'content': data                               # actual product list
        })
