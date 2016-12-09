from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^oauth/$', views.oauth),
]
