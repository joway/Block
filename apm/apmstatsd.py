#!/usr/bin/env python
import statsd as statsd_lib

from config import settings

statsd = statsd_lib.StatsClient(settings.STATSD_HOST, 8125, prefix=settings.STATSD_PREFIX)
