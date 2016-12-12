from django.conf import settings
from django.conf.urls import url
from django_mobile.cache import cache_page

from analysis import views

urlpatterns = [
    url(r'^$', cache_page(settings.CACHES_TIME)(views.index)),
]
