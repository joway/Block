from django.conf.urls import url

from articles import views

urlpatterns = [
    url(r'^$', views.list),
    url(r'^post/$', views.post),
    url(r'^([A-Za-z0-9]+)/$', views.detail),
    url(r'^([A-Za-z0-9]+)/edit/$', views.edit),
]
