from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from articles import views

urlpatterns = [
    url(r'^$', cache_page(settings.CACHES_TIME)(views.list)),
    url(r'^post/$', views.post),
    url(r'^([A-Za-z0-9]+)/$', cache_page(settings.CACHES_TIME)(views.detail), name='article_detail'),
    url(r'^([A-Za-z0-9]+)/edit/$', views.edit),

]
