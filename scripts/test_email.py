from django.core.mail import send_mail


def run(*args):
    try:
        send_mail('Subject here', 'Here is the message.', 'joway@joway.wang',
              ['670425438@qq.com'])
    except Exception as e:
        print(e)

