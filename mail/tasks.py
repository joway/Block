from config.celery import app
from mail.service import MailService


@app.task
def mail_has_commented(comment):
    MailService.sent_email_has_commented(username=comment.user_name,
                                         comment_content=comment)
