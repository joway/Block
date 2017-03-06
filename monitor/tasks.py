from time import sleep

import twitter
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.conf import settings
from weibo import Client

from monitor.constants import MonitorFrequency, ObjectDataType
from monitor.models import MonitorTask, ObjectData
from monitor.services import MonitorService
from utils.baidu_translate import BaiduTranslate

logger = get_task_logger(__name__)


def handle_tasks(tasks):
    for task in tasks:
        logger.info('Monitor task %s has started' % task.name)
        try:
            MonitorService.distribute_task(task)
        except Exception as e:
            logger.error(str(e))
        logger.info('Monitor task %s done' % task.name)


@periodic_task(run_every=(crontab(minute='*/5')),
               name="monitor_5_minute_update", ignore_result=True)
def monitor_5_minute_update():
    logger.info('monitor_5_minute_update  has started')
    tasks = MonitorTask.objects.filter(
        triggered=False,
        frequency=MonitorFrequency.FIVE_MINUTES)
    handle_tasks(tasks)


@periodic_task(run_every=(crontab(minute=0, hour='*/1')),
               name="monitor_1_hour_update", ignore_result=True)
def monitor_1_hour_update():
    logger.info('monitor_1_hour_update  has started')
    tasks = MonitorTask.objects.filter(
        triggered=False,
        frequency=MonitorFrequency.ONE_HOUR)
    handle_tasks(tasks)


@periodic_task(run_every=(crontab(minute=0, hour='*/12')),
               name="monitor_half_day_update", ignore_result=True)
def monitor_half_day_update():
    logger.info('monitor_half_day_update  has started')
    tasks = MonitorTask.objects.filter(
        triggered=False,
        frequency=MonitorFrequency.HALF_DAY)
    handle_tasks(tasks)


@periodic_task(run_every=(crontab(minute='*/5')),
               name="monitor_trump", ignore_result=True)
def monitor_trump():
    REDIRECT_URI = 'http://127.0.0.1:8000/test'
    # c = Client(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, REDIRECT_URI)
    # print(c.authorize_url)
    # c.set_code('647d0955d4baf7ab376bb6f67028e88a')
    # {'uid': '1576273817', 'access_token':'','expires_at': 1491418799, 'remind_in': '2621205'}

    token = {'uid': '1576273817', 'access_token': settings.WEIBO_TRUMP_ACCESS_TOKEN,
             'expires_at': 1491418799,
             'remind_in': '2621205'}

    api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                      consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                      access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
                      access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)

    statuses = api.GetUserTimeline(screen_name='realdonaldtrump', count=82)
    statuses.reverse()
    try:
        for status in statuses:
            twit = status.text
            id_str = status.id_str
            key = 'twitter_id_%s' % id_str
            if ObjectData.objects.filter(key=key).exists():
                continue
            ObjectData.objects.create(key=key, data=id_str, type=ObjectDataType.Twitter)
            translated = ''
            ret = BaiduTranslate.translate(query=twit)
            for i in ret:
                translated += ret[i]

            c = Client(settings.WEIBO_API_KEY, settings.WEIBO_API_SECRET, REDIRECT_URI, token)
            weibo_text = """
%s

%s
                """ % (twit, translated)
            info = c.post('statuses/update', visible=0, status=weibo_text)
            logger.info(str(info))
            sleep(1)
    except Exception as e:
        print(str(e))
        logger.error(str(e))
