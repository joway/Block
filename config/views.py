# coding=utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


def index(request):
    return redirect(to=reverse('articles.views.list'))


def error(request):
    error_msg = request.GET.get('error', '未知错误')
    return render(request, 'error.html', locals())
