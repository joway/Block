from django.conf import settings
from taggit.models import Tag

from analysis.services import TrackingService
from articles.constants import ARTICLE_CATEGORY_CHOICES
from articles.models import Article
from utils.server import server_info


def categories(request):
    all_categories = []
    for category in ARTICLE_CATEGORY_CHOICES:
        all_categories.append({
            'identify': category[0],
            'name': category[1],
            'count': Article.objects.filter(category=category[0]).count()
        })
    context = {'categories': all_categories}

    return context


def tags(request):
    tags = Tag.objects.all()
    context = {'tags': tags}

    return context


def site_info(request):
    context = {
        'analysis': {
            'pageview': TrackingService.pageview_report(),
            'server': server_info(),
        },
        'site': {
            'domain': settings.DOMAIN,
            'cur_full_url': "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
        }
    }
    return context
