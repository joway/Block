from celery.utils.log import get_task_logger

from articles.models import Article, ArticleSimilarity
from config.celery import app
from utils.cosine_similiarity import cosine_similarity

logger = get_task_logger(__name__)


@app.task
def cosine_similarity_update(new_article):
    articles = Article.objects.all()
    for target in articles:
        if target.uid == new_article.uid:
            continue
        cosine = cosine_similarity(new_article.content, target.content)
        cosine += cosine_similarity(new_article.title, target.title)
        a = ArticleSimilarity.objects.create(source=new_article, target=target, cosine=cosine)
        b = ArticleSimilarity.objects.create(source=target, target=new_article, cosine=cosine)
        a.save()
        b.save()
    logger.info('%s done' % new_article.title)


@app.task
def cosine_similarity_init():
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
