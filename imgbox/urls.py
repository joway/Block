from django.conf.urls import url

from imgbox import views

urlpatterns = [
    url(r'^$', views.imgbox),
]
