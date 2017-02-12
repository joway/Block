from rest_framework import routers

from articles.apis import ArticleViewSet
from monitor.apis import MonitorViewSet
from tools.apis import ToolsViewSet

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"tools", ToolsViewSet, base_name="api_tools")
router.register(r"articles", ArticleViewSet, base_name="api_articles")
router.register(r"monitor", MonitorViewSet, base_name="api_monitor")
