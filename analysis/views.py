import json
from collections import OrderedDict

from django.shortcuts import render

from analysis.services import TrackingService


def handle_report(report):
    weekly_data = OrderedDict()

    for k in report:
        weekly_data[k] = report[k]['pageview_stats']['total']

    return json.dumps(weekly_data)


def index(request):
    weekly_report = TrackingService.chart_report(7)
    weekly_data = handle_report(weekly_report)

    monthly_report = TrackingService.chart_report(30)
    monthly_data = handle_report(monthly_report)

    return render(request, "analysis/index.html", locals())
