from django.conf.urls import url

from monitor import views

urlpatterns = [
    url(r'^$', views.monitor_list),
    url(r'^create$', views.monitor_create),
]
