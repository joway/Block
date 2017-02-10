from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from monitor.constants import MonitorFrequency
from monitor.models import MonitorTask
from monitor.services import MonitorService

logger = get_task_logger(__name__)


def handle_tasks(tasks):
    for task in tasks:
        logger.info('Monitor task %s has started' % task.name)
        MonitorService.distribute_task(task)
        logger.info('Monitor task %s done' % task.name)


@periodic_task(run_every=(crontab(minute='*/5')),
               name="monitor_5_minute_update", ignore_result=True)
def monitor_5_minute_update():
    tasks = MonitorTask.objects.filter(frequency=MonitorFrequency.FIVE_MINUTES)
    handle_tasks(tasks)


@periodic_task(run_every=(crontab(hour='*/1')),
               name="monitor_1_hour_update", ignore_result=True)
def monitor_1_hour_update():
    tasks = MonitorTask.objects.filter(frequency=MonitorFrequency.ONE_HOUR)
    handle_tasks(tasks)


@periodic_task(run_every=(crontab(hour='*/12')),
               name="monitor_half_day_update", ignore_result=True)
def monitor_half_day_update():
    tasks = MonitorTask.objects.filter(frequency=MonitorFrequency.HALF_DAY)
    handle_tasks(tasks)
