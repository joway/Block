from django.shortcuts import render


def about(request):
    render(request, 'about/about.html', locals())
