from django.conf.urls import include, url
from django.contrib import admin

from articles.models import ArticleRSSFeed
from config import views
from config.router import router
from config.views import proxy_post_comment

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^tracking/', include('tracking.urls')),
    url(r'^activity/', include('actstream.urls')),

    # local view
    url(r'^$', views.index),
    url(r"^a/", include('articles.urls')),
    url(r"^user/", include('users.urls')),
    url(r'^analysis/', include('analysis.urls')),
    url(r'^timeline/', include('timeline.urls')),
    url(r"^oauth/", include('oauth.urls'), name='oauth'),
    url(r"^about/", include('about.urls')),
    url(r'^imgbox/', include('imgbox.urls')),
    url(r'^feeds/', include('feed.urls')),

    url(r'^search/', include('haystack.urls')),

    url(r'^error/$', views.error),
    url(r'^cache/clear/$', views.cache_clear),
    url(r'^feed/$', ArticleRSSFeed(), name="article_rss"),

    # api
    url(r"^api/", include(router.urls)),
    url(r'^api/comments/post/$', proxy_post_comment, name='comments-post-comment'),
    url(r'^api/comments/', include('django_comments.urls')),

]

handler404 = 'config.views.not_fount'
