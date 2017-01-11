import datetime
from os import walk

from django.utils.dateparse import parse_datetime

from articles.constants import ArticleCategories
from articles.models import Article
from users.models import User
from utils.tag import topk


def run(*args):
    try:
        mypath = '.backup'
        files = []

        author = User.objects.get(email='joway.w@gmail.com')

        for (dirpath, dirnames, filenames) in walk(mypath):
            for f in filenames:
                files.append(dirpath + '/' + f)
            break

        for filename in files:
            with open(filename, 'r', encoding='utf-8') as file:
                data = file.read()
            meta = data.split('---')[1]
            content = ''.join(data.split('---')[2:])
            for line in meta.split('\n'):
                if 'title' in line:
                    title = line.split('title: ')[1].replace('\"', '')
                if 'categories' in line:
                    category = line.split('categories: ')[1].replace('\"', '')
                if 'date' in line:
                    date = line.split('date: ')[1].replace('/', '-')
                    if len(date) > 10:
                        date = date[:10]
                    date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    date = parse_datetime(str(date))

            if Article.objects.filter(title=title).exists():
                continue

            a = Article.objects.create(title=title, author=author, content=content,
                                       category=ArticleCategories.LITERATURE)
            a.created_at = date
            a.tags.add(*topk(content.replace('#', ''), 3))
            a.save()

            print(filename, 'added')
    except Exception as e:
        print(e)
