from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from articles.models import Article
from users.decorators import admin_required


def list(request):
    articles = Article.objects.all()

    page = request.GET.get('page', '1')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')
    print(category)

    if category:
        articles = articles.filter(category=category)
    if tag:
        articles = articles.filter(articletaggeditem__tag__slug__contains=tag)

    print(articles)

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


def detail(request, article_uid):
    article = get_object_or_404(Article, uid=article_uid)

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
