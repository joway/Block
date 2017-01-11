import os

PRODUCTION = False

ENV = {
    'DEBUG': 'True',
    'SECRET_KEY': 'xxxxxx3',
    'MYSQL_HOST': 'xxxx',
    'MYSQL_USERNAME': 'root',
    'MYSQL_PASSWORD': 'xxxxxt',
    'MYSQL_INSTANCE_NAME': 'block',
    'MYSQL_PORT': '3306',
    'SOCIAL_AUTH_GITHUB_KEY': 'xxx',
    'SOCIAL_AUTH_GITHUB_SECRET': 'xxx',
    'SOCIAL_AUTH_WEIBO_KEY': 'xxx',
    'SOCIAL_AUTH_WEIBO_SECRET': 'xxxx',
    'OPBEAT_ORGANIZATION_ID': 'xxx',
    'OPBEAT_APP_ID': 'xxx',
    'OPBEAT_SECRET_TOKEN': 'xxx',
    'QINIU_ACCESS_KEY': 'xxxxx',
    'QINIU_SECRET_KEY': 'xxx',
    'QINIU_STORAGE': 'True',
    'BROKER_URL': 'redis://:xxx@host:6379/0',
    'AWS_ACCESS_KEY_ID': 'xxx',
    'AWS_SECRET_ACCESS_KEY': '7+xxx',
    'EMAIL_HOST_PASSWORD': 'xxxx'
}

for i in ENV.keys():
    os.environ[i] = ENV[i]
