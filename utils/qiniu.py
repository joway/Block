from django.conf import settings
from qiniu import Auth
from qiniu import put_data

access_key = settings.QINIU_ACCESS_KEY
secret_key = settings.QINIU_SECRET_KEY
bucket_name = settings.QINIU_BUCKET_NAME
if settings.QINIU_SECURE_URL:
    static_url = 'https://%s' % settings.QINIU_BUCKET_DOMAIN
else:
    static_url = 'http://%s' % settings.QINIU_BUCKET_DOMAIN

# 构建鉴权对象
q = Auth(access_key, secret_key)


def gen_token(full_key, timeout=3600):
    return q.upload_token(bucket_name, full_key, timeout)


def upload_file(key, data, _prefix='upload/'):
    # 生成上传 Token，可以指定过期时间等
    token = gen_token(_prefix + key)
    ret, info = put_data(token, _prefix + key, data)
    try:
        url = static_url + '/' + ret['key']
    except:
        url = None
    return url
