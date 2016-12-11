import random
import string
from datetime import timedelta, datetime

import pytz
import shortuuid

shortuuid.set_alphabet(string.ascii_uppercase + string.digits)


def get_random_string(length):
    # 0123456789ABCDEFGHJKLMNPQRSTUVWXYZ
    return ''.join([random.choice(string.ascii_uppercase + string.digits)
                    for n in range(length)])


def get_uuid(length):
    return shortuuid.uuid()[:length]


def format_url(url):
    return url


def time_localize(t):
    return pytz.utc.localize(t)


def days_ago(dt, ago):
    today = dt.date()
    _days_ago = today - timedelta(ago)
    start = time_localize(datetime.combine(_days_ago, dt.time()))
    end = time_localize(datetime.combine(today, dt.time()))
    return start, end


def yesterday(dt):
    today = dt.date()
    _days_ago = today - timedelta(1)
    return time_localize(datetime.combine(_days_ago, dt.time()))
