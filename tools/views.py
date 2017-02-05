# Create your views here.
from django.shortcuts import render


def douban_export(request):
    return render(request, 'tools/douban_export.html', locals())
