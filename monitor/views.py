from django.shortcuts import render


def monitor_list(request):
    return render(request, 'monitor/list.html', locals())
