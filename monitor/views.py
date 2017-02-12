from django.shortcuts import render, get_object_or_404

from monitor.models import MonitorTask


def monitor_list(request):
    tasks = MonitorTask.objects.all()
    return render(request, 'monitor/list.html', locals())


def monitor_detail(request, task_id):
    task = get_object_or_404(MonitorTask, id=task_id)
    return render(request, 'monitor/detail.html', locals())


def monitor_create(request):
    return render(request, 'monitor/create.html', locals())
