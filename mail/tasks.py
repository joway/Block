from config.celery import app
from mail.service import MailService


@app.task
def mail_has_commented(username, comment_content):
    MailService.sent_email_has_commented(username=username,
                                         comment_content=comment_content)
