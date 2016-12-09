# coding=utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


def index(request):
    return redirect(to=reverse('articles.views.list'), permanent=True)


def detail(request):
    return render(request, 'articles/detail.html', locals())
