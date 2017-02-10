from django.conf.urls import url

from monitor import views

urlpatterns = [
    url(r'^$', views.monitor_list),
]
