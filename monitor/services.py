import re
from datetime import datetime
from urllib.parse import urlparse

import requests
from django.conf import settings

from mail.service import MailService
from monitor.constants import MonitorType
from utils.render import render_to_html
from utils.server import check_ping


class MonitorService(object):
    @classmethod
    def distribute_task(cls, task, fake=False):
        if task.type in [MonitorType.Contains,
                         MonitorType.NotContains]:
            cls.handle_contains_or_not(task, fake)
        elif task.type == MonitorType.Ping:
            cls.handle_ping(task, fake)
        elif task.type in [
            MonitorType.GreaterThan,
            MonitorType.LessThan,
            MonitorType.EqualTo
        ]:
            cls.handle_compare(task, fake)
        task.updated_at = datetime.now()
        task.save()

    @classmethod
    def extract_html_block(cls, task):
        if task.need_render:
            content = render_to_html(task.link)
        else:
            req = requests.get(task.link)
            content = req.text
        try:
            result = re.findall(task.regex, content)
        except:
            result = ['']
        ele = result[0].replace(' ', '') if result else ''
        task.selected_element = ele
        task.save()
        return ele

    @classmethod
    def handle_contains_or_not(cls, task, fake=False):
        block = cls.extract_html_block(task)
        if fake:
            return
        if task.type == MonitorType.Contains:
            if task.data in block:
                MailService.sent_email_monitor_trigger(
                    to=settings.EMAIL_HOST_USER, task=task)
        else:
            if task.data not in block:
                MailService.sent_email_monitor_trigger(
                    to=settings.EMAIL_HOST_USER, task=task)

    @classmethod
    def handle_compare(cls, task, fake=False):
        block = cls.extract_html_block(task)
        num = float(block)
        data = float(task.data)
        if fake:
            return
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
    def handle_ping(cls, task, fake=False):
        if check_ping(urlparse(task.link).netloc.split(':')[1]):
            if fake:
                return
            MailService.sent_email_monitor_trigger(
                to=settings.EMAIL_HOST_USER, task=task)
