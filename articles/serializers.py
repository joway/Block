from rest_framework import serializers

from articles.models import Article


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('uid', 'title', 'content', 'created_at', 'updated_at', 'author', 'category')


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'content', 'category')
