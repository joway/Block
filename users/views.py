from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


@login_required
def logout(request):
    django_logout(request)
    return redirect(to=reverse('articles.views.list'), permanent=True)
