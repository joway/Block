from actstream.models import Action
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render


def timeline(request):
    actions = Action.objects.all()

    page = request.GET.get('page', '1')

    paginator = Paginator(actions, settings.PAGING_SIZE * 2)
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        actions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        actions = paginator.page(paginator.num_pages)

    return render(request, 'timeline/index.html', locals())
