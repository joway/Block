from actstream.models import Action
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from users.models import User


def timeline(request):
    title = '时间线'

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


def my_friends(request):
    friends = User.objects.filter(is_superuser=False,
                                  github_username__isnull=False).all()
    return render(request, 'timeline/friends.html', locals())
