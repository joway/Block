from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render


def about_me(request):
    about_title = 'About Me'
    about_path = settings.BASE_DIR + '/about.md'
    with open(about_path, encoding='utf-8') as file:
        about_content = file.read()
    comment_obj = Site.objects.get(id=settings.SITE_ID)

    return render(request, 'about/about.html', locals())


def about_site(request):
    about_title = 'About Title'
    about_path = settings.BASE_DIR + '/README.md'
    with open(about_path, encoding='utf-8') as file:
        about_content = file.read()
    comment_obj = Site.objects.get(id=settings.SITE_ID)

    return render(request, 'about/about.html', locals())
