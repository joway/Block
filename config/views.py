# coding=utf-8
import requests
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django_comments.views.comments import post_comment, CommentPostBadRequest

from analysis.services import ActionService
from articles.views import list as article_list
from mail.tasks import mail_has_commented
from users.decorators import admin_required


def index(request):
    return article_list(request)


def robots(request):
    with open('robots.txt', 'rb') as f:
        data = f.read()
    return HttpResponse(data, content_type='text/plain')


def error(request):
    title = '错误'

    error_msg = request.GET.get('error', '未知错误')
    return render(request, 'error.html', locals())


def not_fount(request):
    title = 'Not Found'

    return render(request, '404.html', locals())


def server_error(request):
    title = 'Server Error'

    return render(request, '500.html', locals())


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

    if not request.user.is_admin:
        ActionService.comment(request.user, target)
    return post_comment(request, next, using)


@login_required
@admin_required
def cache_clear(request):
    next = request.GET.get('next', '/')
    cache.clear()
    return HttpResponseRedirect(redirect_to=next)


def search(request):
    query = request.GET.get('q', '')
    tag = request.GET.get('t', '')
    return render(request, 'search.html', locals())


def doubanshow(request):
    book_req = requests.get('https://api.douban.com/v2/book/user/54019708/collections',
                            params={'status': 'read'})
    books = book_req.json()['collections']
    return render(request, 'douban.html', locals())
