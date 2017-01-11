# coding=utf-8
from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django_comments.views.comments import post_comment, CommentPostBadRequest
from mail.tasks import mail_has_commented

from analysis.services import ActionService
from articles.models import Article
from users.decorators import admin_required


def index(request):
    articles = Article.objects.all()

    page = request.GET.get('page', '1')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')

    if category:
        articles = articles.filter(category=category)
    if tag:
        articles = articles.filter(articletaggeditem__tag__slug__contains=tag)

    paginator = Paginator(articles, settings.PAGING_SIZE)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(request, 'articles/list.html', locals())


def error(request):
    error_msg = request.GET.get('error', '未知错误')
    return render(request, 'error.html', locals())


def not_fount(request):
    return render(request, '404.html', locals())


@csrf_protect
@require_POST
def proxy_post_comment(request, next=None, using=None):
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = apps.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
    except TypeError:
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % (
                escape(ctype), escape(object_pk)))
    except (ValueError, ValidationError) as e:
        return CommentPostBadRequest(
            "Attempting go get content-type %r and object PK %r exists raised %s" % (
                escape(ctype), escape(object_pk), e.__class__.__name__))

    mail_has_commented.delay(request.user.username, data['comment'])
    ActionService.comment(request.user, target)
    return post_comment(request, next, using)


@login_required
@admin_required
def cache_clear(request):
    next = request.GET.get('next', '/')
    cache.clear()
    return HttpResponseRedirect(redirect_to=next)
