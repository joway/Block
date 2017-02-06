from django.conf.urls import url

from articles import views

urlpatterns = [
    url(r'^$', views.list),
    url(r'^post/$', views.post),
    url(r'^(?P<slug_or_uid>[-\w]+)/$', views.detail),
    url(r'^(?P<slug_or_uid>[-\w]+)/edit/$', views.edit),
]
