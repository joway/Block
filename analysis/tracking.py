from datetime import datetime

from analysis.constants import ANALYSITICS_METRICS
from analysis.google_analytics import get_ga_report


def tracking_report(start_time, end_time):
    report = get_ga_report(datetime.strftime(start_time, '%Y-%m-%d'),
                           datetime.strftime(end_time, '%Y-%m-%d'))
    visitor_stats = report.get(ANALYSITICS_METRICS.USERS)
    pageview_stats = report.get(ANALYSITICS_METRICS.PAGE_VIEW)

    return {
        'visitor_stats': visitor_stats,
        'pageview_stats': pageview_stats,
    }
