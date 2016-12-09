from django.conf.urls import url

from articles import views

urlpatterns = [
    url(r'^$', views.list),
    url(r'^(\d+)/$', views.detail),
    url(r'^(\d+)/edit/$', views.edit),

]
