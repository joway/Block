from django.contrib import admin

# Register your models here.
from monitor.models import MonitorTask

admin.site.register(MonitorTask)
