from django.shortcuts import render


# Create your views here.

def social(request):
    path = request.GET.get('next', '')
    return render(request, 'oauth/social.html', locals())
