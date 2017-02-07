# Create your views here.
import os

from django.conf import settings
from django.shortcuts import render


def gallery_list(request):
    base_url = settings.STATIC_URL + 'gallery/'
    albums = []
    for root, dirs, files in os.walk("static/gallery/"):
        album = root.split('/')[2]
        if not album:
            continue
        cover = '%s.jpeg' % album
        albums.append({
            'name': album,
            'cover': base_url + cover,
        })
    return render(request, 'gallery/list.html', locals())


def gallery_detail(request, album):
    base_url = settings.STATIC_URL
    images = []
    for root, dirs, files in os.walk("static/gallery/%s" % album):
        for name in files:
            if os.path.splitext(name)[1] == '.jpg' or os.path.splitext(name)[1] == '.jpeg':
                url = '%s%s/%s/%s?imageView2/2/w/1000' % (base_url, 'gallery', album, name)
                images.append(url)
    return render(request, 'gallery/detail.html', locals())
