from django.contrib import admin

from monitor.models import MonitorTask


class MonitorTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'regex',
                    'type', 'data', 'frequency',
                    'triggered']

    class Meta:
        model = MonitorTask


admin.site.register(MonitorTask, MonitorTaskAdmin)
