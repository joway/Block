import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class ProxyPool(object):
    KUAIDAILI_API = 'http://www.kuaidaili.com/proxylist/%s/'

    HEADERS = {
        'Referer': 'http://www.kuaidaili.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2692.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    POOL = {}
    SSL = True
    last_update = datetime.now()

    @classmethod
    def random_proxy(cls):
        _pool = cls.get_pool()
        random_ip = random.choice(list(_pool.keys()))
        return random_ip, _pool[random_ip]

    @classmethod
    def get_pool(cls):
        if not cls.POOL or (datetime.now() - cls.last_update).seconds > 60 * 10:
            cls.update()
        return cls.POOL

    @classmethod
    def update(cls, page=3):
        _pool = {}
        for i in range(1, page + 1):
            _html = requests.get(cls.KUAIDAILI_API % i,
                                 headers=cls.HEADERS).text
            soup = BeautifulSoup(_html, 'lxml')
            ip_list = soup.select('tbody tr')
            for ip_tr in ip_list:
                ip = ip_tr.find(attrs={"data-title": "IP"}).string
                port = ip_tr.find(attrs={"data-title": "PORT"}).string
                protocol = ip_tr.find(attrs={"data-title": "类型"}).string
                print(protocol)
                if cls.SSL and 'HTTPS' not in protocol:
                    continue
                _pool[ip] = port
        cls.POOL = _pool
        return _pool

