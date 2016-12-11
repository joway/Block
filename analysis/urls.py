from django.conf.urls import url

from analysis import views

urlpatterns = [
    url(r'^$', views.index),
]
