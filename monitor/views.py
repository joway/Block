# Create your views here.
from django.shortcuts import render


def air(request):
    return render(request, 'monitor/air.html', locals())
