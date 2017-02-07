from django.conf.urls import url

from gallery import views

urlpatterns = [
    url(r'^$', views.gallery_list),
    url(r'^(?P<album>[-\w]+)/$', views.gallery_detail),
]
