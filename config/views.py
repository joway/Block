# coding=utf-8
from django.conf import settings
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render

from articles.models import Article


def index(request):
    articles = Article.objects.all()

    page = request.GET.get('page', '1')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')

    if category:
        articles = articles.filter(catalog=category)
    if tag:
        articles = articles.filter(articletaggeditem__tag__slug__contains=tag)

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


def error(request):
    error_msg = request.GET.get('error', '未知错误')
    return render(request, 'error.html', locals())
