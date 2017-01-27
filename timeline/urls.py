from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^friends/$', views.my_friends),
    url(r'^$', views.timeline),
]
