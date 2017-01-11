from django.core.mail import send_mail

from config import settings


class MailService(object):
    @classmethod
    def sent_email_has_commented(cls, username, comment_content):
        send_mail(
            subject='[城西笔谈] 您有一个来自%s新的评论 ' % username,
            message=comment_content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['joway.w@gmail.com'])

    @classmethod
    def sent_email_comment_reply(cls, to):
        send_mail(
            subject='[城西笔谈] 您的评论已被回复 ',
            message='Here is the message.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to])
