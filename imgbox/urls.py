from django.conf.urls import url

from imgbox import views

urlpatterns = [
    url(r'^$', views.imgbox),
    url(r'^api/$', views.imgbox_api),
]
