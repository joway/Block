import json
from collections import OrderedDict

from django.core.cache import cache
from django.shortcuts import render

from analysis.services import TrackingService


def handle_report(report):
    weekly_data = OrderedDict()

    for k in report:
        weekly_data[k] = report[k]['pageview_stats']

    return json.dumps(weekly_data)


def index(request):
    title = '统计分析'

    weekly_report = cache.get('weekly_report')
    if not weekly_report:
        weekly_report = TrackingService.chart_report(7)
        cache.set('weekly_report', weekly_report, 60 * 60 * 24)

    weekly_data = cache.get('weekly_data')
    if not weekly_data:
        weekly_data = handle_report(weekly_report)
        cache.set('weekly_data', weekly_data, 60 * 60 * 24)

    monthly_report = cache.get('monthly_report')
    if not monthly_report:
        monthly_report = TrackingService.chart_report(30)
        cache.set('monthly_report', monthly_report, 60 * 60 * 24)

    monthly_data = cache.get('monthly_data')
    if not monthly_data:
        monthly_data = handle_report(monthly_report)
        cache.set('monthly_data', monthly_data, 60 * 60 * 24)

    return render(request, "analysis/index.html", locals())
