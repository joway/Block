from django.conf.urls import include, url
from django.contrib import admin

from config import views
from config.router import router

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^error/$', views.error),

    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^tracking/', include('tracking.urls')),
    url(r'^activity/', include('actstream.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r"^user/", include('users.urls')),
    url(r"^a/", include('articles.urls')),
    url(r"^oauth/", include('oauth.urls'), name='oauth'),
    url(r"^about/", include('about.urls')),

    url(r"^api/", include(router.urls)),
    url(r'^api/comments/', include('django_comments.urls')),
]
