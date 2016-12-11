from django.shortcuts import render

from users.models import User


def timeline(request):
    admin = User.objects.filter(is_superuser=True, is_staff=True).first()
    return render(request, 'timeline/index.html', locals())
