from django.contrib.auth import authenticate, login as django_login
from django.shortcuts import render

from users.forms import SignInForm
from users.models import User


def login(request):
    signin_form = SignInForm()
    from_path = request.GET.get('next', '')
    if request.method != 'POST':
        return render(request, 'login.html' + '?next=' + from_path, locals())

    from_path = request.POST.get('next', '')
    signin_form = SignInForm(request.POST)
    if not signin_form.is_valid():
        return render(request, 'login.html', locals())

    email = signin_form.cleaned_data['email']
    password = signin_form.cleaned_data['password']

    try:
        user = authenticate(email=email, password=password)
        if not user:
            return render(request, 'login.html', locals())
    except User.DoesNotExist:
        return render(request, 'register.html', locals())

    django_login(request, user)
    return render(request, 'success.html', locals())


def oauth(request):
    from_path = request.GET.get('next', '')
    if request.method == 'GET':
        return render(request, 'oauth.html', locals())
