from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render


def index(request):
    about_path = settings.BASE_DIR + '/about.md'
    with open(about_path, encoding='utf-8') as file:
        about_content = file.read()
    comment_obj = Site.objects.get(id=settings.SITE_ID)

    return render(request, 'about/about.html', locals())
