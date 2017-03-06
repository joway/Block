import hashlib
import random
from collections import OrderedDict

import requests

# public api key
APPID = '20151113000005349'
APPKEY = 'osubCEzlGjzvw8qdQc41'

BAIDU_TRANS_API = 'http://api.fanyi.baidu.com/api/trans/vip/translate'


class BaiduTranslate(object):
    @classmethod
    def salt(cls, start=32768, end=65536):
        return random.randint(start, end)

    @classmethod
    def sign(cls, appid, query, salt, key):
        m = hashlib.md5()
        m.update((str(appid) + query + str(salt) + key).encode('utf-8'))
        # 32 位 md5值
        return m.hexdigest()

    @classmethod
    def translate(cls, query, fr='auto', to='zh'):
        salt = cls.salt()
        payload = {'q': query,
                   'from': fr,
                   'to': to,
                   'appid': APPID,
                   'salt': salt,
                   'sign': cls.sign(APPID, query, salt, APPKEY)}
        r = requests.get(BAIDU_TRANS_API, params=payload)
        return cls.parse(r.json())

    @classmethod
    def en_to_zh(cls, query):
        return cls.translate(query, fr='en', to='zh')

    @classmethod
    def zh_to_en(cls, query):
        return cls.translate(query, fr='zh', to='en')

    @classmethod
    def parse(cls, response):
        result = OrderedDict()
        try:
            for i in response['trans_result']:
                result[i['src']] = i['dst']
        except KeyError:
            cls.log('error : ' +
                    response['error_code'] + ":  " + response['error_msg'])
            return response['error_code'], response['error_msg']
        # cls.log('success : ' + str(response))
        return result

    @classmethod
    def log(cls, msg):
        print(msg)
