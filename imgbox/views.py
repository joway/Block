import json
import os
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from users.decorators import admin_required
from utils.qiniu import upload_file


@login_required
@admin_required
def imgbox(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
        except:
            return render(request, 'imgbox/index.html', locals())
        ext = os.path.splitext(file.name)[1]
        file_url = upload_file(key=str(int(time.time() * 10)) + ext, data=file.read())
    return render(request, 'imgbox/index.html', locals())


@login_required
@admin_required
@require_POST
def imgbox_api(request):
    try:
        file = request.FILES['file']
    except:
        return HttpResponse(json.dumps({'error': '缺少文件file参数'}))
    ext = os.path.splitext(file.name)[1]
    file_url = upload_file(key=str(int(time.time() * 10)) + ext, data=file.read())
    return HttpResponse(json.dumps({'url': file_url}))
