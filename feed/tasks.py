import feedparser
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.utils.dateparse import parse_datetime
from django.utils.datetime_safe import datetime

from feed.models import Feed, FeedStream

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/30')),
               name="feed_update", ignore_result=True)
def feed_update():
    feeds = Feed.objects.all()

    for feed in feeds:
        resp = feedparser.parse(feed.url)
        for entry in resp['entries']:
            try:
                author = entry['author']
            except KeyError:
                author = '匿名'
            try:
                title = entry['title_detail']['value']
            except KeyError:
                title = '未知'

            try:
                created_at = parse_datetime(entry['updated'])
            except KeyError:
                created_at = parse_datetime(str(datetime.now()))

            try:
                link = entry['link']
            except KeyError as e:
                logger.error(str(e))
                return

            try:
                content = entry['summary_detail']['value']
            except KeyError:
                content = ''

            if not FeedStream.objects.filter(link=link).exists():
                stream = FeedStream.objects.create(author=author,
                                                   created_at=created_at,
                                                   link=link,
                                                   content=content,
                                                   feed=feed,
                                                   title=title)
                if not stream.created_at:
                    stream.created_at = stream.indexed_at
                stream.save()
                logger.info('%s Added' % title)
