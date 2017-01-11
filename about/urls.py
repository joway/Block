from django.conf.urls import url

from about import views

urlpatterns = [
    url(r'^site/$', views.about_site),
    url(r'^$', views.about_me),
]
