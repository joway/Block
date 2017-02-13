from django.db import models

from monitor.constants import MONITOR_FREQUENCY_CHOICES, MonitorFrequency, MONITOR_TYPE_CHOICES
from monitor.services import MonitorService


class MonitorTask(models.Model):
    name = models.CharField('名称', max_length=255)
    link = models.URLField('监控链接')
    regex = models.CharField('正则表达式', max_length=255)
    data = models.CharField(max_length=512, default='')
    type = models.IntegerField(choices=MONITOR_TYPE_CHOICES)
    frequency = models.IntegerField(choices=MONITOR_FREQUENCY_CHOICES, default=MonitorFrequency.ONE_HOUR)

    triggered = models.BooleanField('被触发', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def element(self):
        return MonitorService.extract_html_block(self)
