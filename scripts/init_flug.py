from django.core.mail import send_mail

from articles.models import Article


def run(*args):
    articles = Article.objects.all()
    for a in articles:
        a.save()

