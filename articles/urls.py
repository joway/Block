from django.conf.urls import url

from articles import views

urlpatterns = [
    url(r'^$', views.list),
    url(r'^post/$', views.post),
    url(r'^(?P<title_or_uid>[-\w]+)/$', views.detail),
    url(r'^([A-Za-z0-9]+)/edit/$', views.edit),
]
