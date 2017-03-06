# Create your views here.
import json
import os

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render


def gallery_list(request):
    base_url = settings.STATIC_URL + 'gallery/'
    title = '画廊 | 文一西路 : Joway 的摄影人生'
    meta_description = title

    if request.flavour == 'mobile':
        width = 256
    else:
        width = 600
    cache_key = 'galery#list#%s' % request.flavour
    _cache = cache.get(cache_key)
    if _cache:
        albums = json.loads(_cache)
        meta_keywords = ', '.join(['文一西路', '画廊', '摄影'] + [x['name'] for x in albums])
        return render(request, 'gallery/list.html', locals())

    albums = []
    for root, dirs, files in os.walk("static/gallery/"):
        album = root.split('/')[2]
        if not album:
            continue
        cover = '%s.jpeg?imageView2/2/w/%s/interlace/1' % (album, width)
        albums.append({
            'name': album,
            'cover': base_url + cover,
        })
    cache.set(cache_key, json.dumps(albums), 3600)
    meta_keywords = ', '.join(['文一西路', '画廊', '摄影'] + [x['name'] for x in albums])
    return render(request, 'gallery/list.html', locals())


def gallery_detail(request, album):
    base_url = settings.STATIC_URL
    title = '画廊 ： %s | 文一西路' % album
    meta_description = title

    if request.flavour == 'mobile':
        width = 256
    else:
        width = 1000
    cache_key = 'galery#%s#%s' % (album, request.flavour)
    _cache = cache.get(cache_key)
    if _cache:
        images = json.loads(_cache)
        return render(request, 'gallery/detail.html', locals())

    images = []
    for root, dirs, files in os.walk("static/gallery/%s" % album):
        for name in files:
            if os.path.splitext(name)[1] == '.jpg' or os.path.splitext(name)[1] == '.jpeg':
                url = '%s%s/%s/%s?imageView2/2/w/%s/interlace/1' % (base_url, 'gallery', album, name, width)
                images.append(url)

    cache.set(cache_key, json.dumps(images), 3600)
    return render(request, 'gallery/detail.html', locals())
