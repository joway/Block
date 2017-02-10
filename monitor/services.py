import re
from urllib.parse import urlparse

import requests
from django.conf import settings

from mail.service import MailService
from monitor.constants import MonitorType
from utils.server import check_ping


class MonitorService(object):
    @classmethod
    def distribute_task(cls, task):
        if task.type in [MonitorType.Contains,
                         MonitorType.NotContains]:
            cls.handle_contains_or_not(task)
        elif task.type == MonitorType.Ping:
            cls.handle_ping(task)
        elif task.type in [
            MonitorType.GreaterThan,
            MonitorType.LessThan,
            MonitorType.EqualTo
        ]:
            cls.handle_compare(task)

    @classmethod
    def extract_html_block(cls, task):
        req = requests.get(task.link)
        result = re.findall(task.regex, req.text)
        return result[0] if result else ''

    @classmethod
    def handle_contains_or_not(cls, task):
        block = cls.extract_html_block(task)
        if task.type == MonitorType.Contains:
            if task.data in block:
                MailService.sent_email_monitor_trigger(
                    to=settings.EMAIL_HOST_USER, task=task)
        else:
            if task.data not in block:
                MailService.sent_email_monitor_trigger(
                    to=settings.EMAIL_HOST_USER, task=task)

    @classmethod
    def handle_compare(cls, task):
        block = cls.extract_html_block(task)
        num = int(block)
        data = int(task.data)
        if task.type == MonitorType.EqualTo:
            if num == data:
                MailService.sent_email_monitor_trigger(
                    to=settings.EMAIL_HOST_USER, task=task)
        elif task.type == MonitorType.GreaterThan:
            if num > data:
                MailService.sent_email_monitor_trigger(
                    to=settings.EMAIL_HOST_USER, task=task)
        elif task.type == MonitorType.LessThan:
            if num < data:
                MailService.sent_email_monitor_trigger(
                    to=settings.EMAIL_HOST_USER, task=task)
        else:
            raise Exception

    @classmethod
    def handle_ping(cls, task):
        if check_ping(urlparse(task.link).netloc.split(':')[1]):
            MailService.sent_email_monitor_trigger(
                to=settings.EMAIL_HOST_USER, task=task)
