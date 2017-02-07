from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page
from django_statsd.urls import urlpatterns as statsd_patterns

from articles.models import ArticleRSSFeed, Article
from config import views
from config.router import router
from config.views import proxy_post_comment

admin.autodiscover()

sitemaps = {
    'article': GenericSitemap({
        'queryset': Article.objects.all(), 'date_field': 'created_at'
    }, priority=0.6),
}

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', cache_page(60 * 60 * 12)(sitemap), {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^activity/', include('actstream.urls')),
    url(r'^gallery/', include('gallery.urls')),

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
    url(r'^tools/', include('tools.urls')),

    url(r'^error/$', views.error),
    url(r'^cache/clear/$', views.cache_clear),
    url(r'^search/$', views.search),

    url(r'^feed/$', ArticleRSSFeed(), name="article_rss"),
    url(r'^life/$', cache_page(60 * 60 * 12)(views.doubanshow), name="douban"),
    url(r'^robots.txt$', views.robots, name="robots"),

    # api
    url(r"^api/", include(router.urls)),
    url(r'^api/comments/post/$', proxy_post_comment, name='comments-post-comment'),
    url(r'^api/comments/', include('django_comments.urls')),

    url('^services/timing/', include(statsd_patterns)),

]

handler404 = 'config.views.not_fount'
