from utils.qiniu import refresh


def run(*args):
    data = {
        "urls": [
            'https://static.joway.wang/static/dist/lib.css',
            'https://static.joway.wang/static/css/index.css',
            'https://static.joway.wang/static/dist/lib.js',
            'https://static.joway.wang/static/dist/index.js',
            'https://static.joway.wang/static/dist/kaomoji.json'
        ]
    }

    _json = refresh(data)
    if _json['code'] == 200:
        print('更新成功: \n' + str(data))
    else:
        print(_json)
