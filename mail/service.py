from django.core.mail import send_mail

from config import settings


class MailService(object):
    @classmethod
    def sent_email_has_commented(cls, username, comment_content):
        send_mail(
            subject='[城西笔谈] 您有一个来自 %s 的新评论 ' % username,
            message="""
            %s :

                %s

            """ % (username, comment_content),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['joway.w@gmail.com'])

    @classmethod
    def sent_email_comment_reply(cls, to):
        send_mail(
            subject='[城西笔谈] 您的评论已被回复 ',
            message='您的评论已被回复.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to])

    @classmethod
    def sent_email_monitor_trigger(cls, to, task):
        send_mail(
            subject='[城西笔谈] 您的监控任务 %s 已触发更新 ' % task.name,
            message="""
            尊敬的用户 :

                您好

                您创建的监控任务 <a href='%s'>%s</a> 已触发更新 。

                请登陆 <a href='https://joway.wang/monitor/task/%s'>%s | 城西笔谈 - 监控 </a> 进行查看 。


            """ % (task.link, task.name, task.id, task.name),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to])
