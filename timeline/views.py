from django.http import HttpResponseRedirect
from django.shortcuts import render

from users.models import User


def timeline(request):
    try:
        admin = User.objects.filter(is_superuser=True, is_staff=True).first()
    except:
        error_msg = '尚未存在管理员帐号'
        return HttpResponseRedirect('/error/?error=%s' % error_msg)

    return render(request, 'timeline/index.html', locals())
