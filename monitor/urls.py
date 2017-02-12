from django.conf.urls import url

from monitor import views

urlpatterns = [
    url(r'^$', views.monitor_list),
    url(r'^create$', views.monitor_create),
    url(r'^task/(?P<task_id>[-\d]+)/$', views.monitor_detail),
]
