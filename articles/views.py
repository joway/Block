from django.shortcuts import render


# Create your views here.
def list(request):
    articles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return render(request, 'articles/list.html', locals())


def detail(request, article_id):
    article = 1
    return render(request, 'articles/detail.html', locals())


def edit(request, article_id):
    return render(request, 'articles/edit.html', locals())
