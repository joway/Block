import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from articles.models import Article
from users.decorators import admin_required


def list(request):
    articles = Article.objects.all()

    page = request.GET.get('page', '1')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')

    if tag or category:
        meta_keywords = ', '.join([category, tag])

    _cache = cache.get('list#%s' % str(request.GET))
    if not _cache:
        if category:
            articles = articles.filter(category=category)
        if tag:
            articles = articles.filter(articletaggeditem__tag__name__contains=tag)
    else:
        articles = _cache

    paginator = Paginator(articles, settings.PAGING_SIZE)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(request, 'articles/list.html', locals())


def detail(request, slug_or_uid):
    _cache = cache.get('detail#%s' % slug_or_uid)

    if _cache:
        article = _cache
    else:
        try:
            article = Article.objects.get(slug=slug_or_uid)
        except Article.DoesNotExist:
            article = get_object_or_404(Article, uid=slug_or_uid)

    meta_description = article.digest
    meta_keywords = ', '.join(article.tag_list())

    title = article.title
    comment_obj = article

    return render(request, 'articles/detail.html', locals())


@login_required
@admin_required
def edit(request, article_uid):
    article = get_object_or_404(Article, uid=article_uid)

    return render(request, 'articles/edit.html', locals())


@login_required
@admin_required
def post(request):
    return render(request, "articles/post.html", locals())
