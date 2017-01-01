import os
import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.decorators import admin_required
from utils.qiniu import upload_file


@login_required
@admin_required
def imgbox(request):
    if request.method == 'POST':
        file = request.FILES['file']
        ext = os.path.splitext(file.name)[1]
        file_url = upload_file(key=str(int(time.time() * 10)) + ext, data=file.read())

    return render(request, 'imgbox/index.html', locals())
