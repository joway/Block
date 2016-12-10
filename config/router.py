from rest_framework import routers

from articles.apis import ArticleViewSet

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"articles", ArticleViewSet, base_name="api_articles")
