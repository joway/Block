from collections import OrderedDict
from datetime import datetime

from actstream import action
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone

from analysis.constants import ActivityType
from analysis.tracking import tracking_report
from utils.helpers import days_ago, yesterday


class ActionService(object):
    @classmethod
    def comment(cls, user, obj):
        action.send(user, verb=ActivityType.COMMENT, target=user.groups.first(), action_object=obj)

    @classmethod
    def post(cls, user, obj):
        action.send(user, verb=ActivityType.POST, target=user.groups.first(), action_object=obj)

    @classmethod
    def login(cls, user):
        site = Site.objects.get(id=settings.SITE_ID)
        action.send(user, verb=ActivityType.LOGIN, target=user.groups.first(), action_object=site)


class TrackingService(object):
    @classmethod
    def chart_report(cls, days):
        now = timezone.now()
        reports = OrderedDict()
        cur = now
        for d in range(days):
            _yesterday = yesterday(cur)
            reports[str(cur.date().strftime('%Y-%m-%d'))] = tracking_report(_yesterday, cur)
            cur = _yesterday

        _reports = OrderedDict()
        for i in range(days):
            k, v = reports.popitem(last=True)
            _reports[k] = v

        return _reports

    @classmethod
    def pageview_report(cls):
        now = timezone.now()

        # daily
        day_start, day_end = days_ago(now, 1)
        daily = tracking_report(day_start, day_end)
        # weekly
        week_start, week_end = days_ago(now, 7)
        weekly = tracking_report(week_start, week_end)

        # monthly
        month_start, month_end = days_ago(now, 30)
        monthly = tracking_report(month_start, month_end)

        # total
        # determine when tracking began
        track_start_time = datetime.strptime('2016-01-01', '%Y-%m-%d')
        total = tracking_report(track_start_time, now)
        return {
            'PV_DAILY': daily['pageview_stats'],
            'UV_DAILY': daily['visitor_stats'],
            'PV_WEEKLY': weekly['pageview_stats'],
            'UV_WEEKLY': weekly['visitor_stats'],
            'PV_MONTHLY': monthly['pageview_stats'],
            'UV_MONTHLY': monthly['visitor_stats'],
            'PV_TOTAL': total['pageview_stats'],
            'UV_TOTAL': total['visitor_stats'],
        }
