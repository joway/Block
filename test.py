import requests

proxies = {
    "http": "http://%s" % '112.74.72.1:8080',
    "https": "http://%s" % '112.74.72.1:8080',
}

data = requests.get('https://www.v2ex.com/t/252139', proxies=proxies)
print(data.text)

