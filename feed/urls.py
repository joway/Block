from django.conf.urls import url

from feed import views

urlpatterns = [
    url(r'^$', views.feed),
]
