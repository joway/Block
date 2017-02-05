from django.conf.urls import url

from tools import views

urlpatterns = [
    url(r'^douban/$', views.douban_export),
]
