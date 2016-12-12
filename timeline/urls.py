from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    url(r'^$', cache_page(settings.CACHES_TIME)(views.timeline)),
]
