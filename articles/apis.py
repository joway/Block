from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from analysis.services import ActionService
from .models import Article
from .paginations import ArticlePagination
from .serializers import ArticleModelSerializer, ArticleCreateSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = ArticlePagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_post=True)
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)

        ActionService.post(request.user, serializer.instance)

        return Response(self.get_serializer(instance=serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ArticleCreateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        ActionService.update(request.user, serializer.instance)

        return Response(self.get_serializer(instance=serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)
