from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from articles.models import Article
from utils.cosine_similiarity import cosine_similarity

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour='*/12')),
               name="article_cosine_similarity", ignore_result=True)
def article_cosine_similarity():
    articles = Article.objects.all()
    BASE_DIR = 'data/similarity/'
    for source in articles:
        data = ''
        for target in articles:
            if target.uid == source.uid:
                continue
            cosine = cosine_similarity(source.content, target.content)
            data += '%s %s' % (target.uid, cosine)
        with open(BASE_DIR + source.uid + '.data', 'w') as file:
            file.write(data)
