from django.conf import settings
from tracking.models import Visitor, Pageview


def tracking_report(start_time, end_time):
    user_stats = Visitor.objects.user_stats(start_time, end_time)
    visitor_stats = Visitor.objects.stats(start_time, end_time)
    if settings.TRACK_PAGEVIEWS:
        pageview_stats = Pageview.objects.stats(start_time, end_time)
    else:
        pageview_stats = None

    return {
        'user_stats': user_stats,
        'visitor_stats': visitor_stats,
        'pageview_stats': pageview_stats,
    }
