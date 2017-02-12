from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from articles.models import Article, ArticleSimilarity
from utils.cosine_similiarity import cosine_similarity

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*/59')),
               name="article_cosine_similarity", ignore_result=True)
def article_cosine_similarity():
    articles = Article.objects.all()
    for source in articles:
        for target in articles:
            if ArticleSimilarity.objects.filter(source=source, target=target).exists():
                continue
            if target.uid == source.uid:
                continue
            cosine = cosine_similarity(source.content, target.content)
            cosine += cosine_similarity(source.title, target.title)
            a = ArticleSimilarity.objects.create(source=source, target=target, cosine=cosine)
            a.save()

        logger.info('%s done' % source.title)
