from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from articles.constants import ARTICLE_CATEGORY_CHOICES
from articles.models import Article
from users.decorators import admin_required


def list(request):
    articles = Article.objects.filter(visible=True).all()

    page = request.GET.get('page', '1')
    category = request.GET.get('category', '')
    if category:
        category_display = [x for x in ARTICLE_CATEGORY_CHOICES if x[0] == category][0][1]
        title = '目录: %s | 文一西路' % category_display
        meta_description = title
        meta_keywords = ', '.join([category_display, '文一西路', '博客'])

    _cache = cache.get('list#%s' % str(request.GET))
    if not _cache:
        if category:
            articles = articles.filter(category=category)
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
        cache.set('detail#%s' % slug_or_uid, article, 3600)

    meta_description = article.digest()
    meta_keywords = ', '.join([article.get_category_display(), '文一西路', article.title])

    title = article.title
    comment_obj = article

    similar_cache = cache.get('article#similay#%s' % slug_or_uid)
    if similar_cache:
        similar_articles = similar_cache
    else:
        similar_articles = [a.target for a in article.similar_articles()]
        cache.set('article#similay#%s' % slug_or_uid, similar_articles, 36000)

    return render(request, 'articles/detail.html', locals())


@login_required
@admin_required
def edit(request, slug_or_uid):
    try:
        article = Article.objects.get(slug=slug_or_uid)
    except Article.DoesNotExist:
        article = get_object_or_404(Article, uid=slug_or_uid)

    return render(request, 'articles/edit.html', locals())


@login_required
@admin_required
def post(request):
    return render(request, "articles/post.html", locals())
