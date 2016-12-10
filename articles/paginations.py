from rest_framework import pagination


class ArticlePagination(pagination.PageNumberPagination):
    ordering = "-created_at"
    page_size_query_param = 'page_size'
    page_size = 10
