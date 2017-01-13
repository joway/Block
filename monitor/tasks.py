from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/30')),
               name="feed_update", ignore_result=True)
def air_update():
    pass
