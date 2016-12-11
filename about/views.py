from django.conf import settings
from django.shortcuts import render


def index(request):
    about_path = settings.BASE_DIR + '/about.md'
    with open(about_path, encoding='utf-8') as file:
        about_content = file.read()

    return render(request, 'about/about.html', locals())
