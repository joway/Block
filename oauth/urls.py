from django.conf.urls import url

from oauth import views

urlpatterns = [
    url(r'^$', views.index, name='begin'),
    url(r'^social/$', views.social),
    url(r'^github/$', views.callback_github, name='oauth_github'),
]
