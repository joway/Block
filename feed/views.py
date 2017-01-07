# Create your views here.
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from feed.models import FeedStream


def feed(request):
    streams = FeedStream.objects.all()

    page = request.GET.get('page', '1')

    paginator = Paginator(streams, settings.PAGING_SIZE * 2)
    try:
        streams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        streams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        streams = paginator.page(paginator.num_pages)
    return render(request, 'feed/index.html', locals())
