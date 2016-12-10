from django.conf.urls import url

from oauth import views

urlpatterns = [
    url(r'^$', views.social),
]
