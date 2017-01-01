import hashlib

import shortuuid

basedigits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
BASE = len(basedigits)


def url_hash(url, length=8):
    return hashlib.md5(url.encode('utf-8')).hexdigest()[:length]


def gen_uuid(length=12):
    return shortuuid.ShortUUID().random(length=length)


def base62_decode(s: str):
    ret, mult = 0, 1
    for c in reversed(s):
        ret += mult * basedigits.index(c)
        mult *= BASE
    return ret


def base62_encode(num: int):
    if num < 0:
        return ''
    if num == 0:
        return '0'
    ret = ''
    while num != 0:
        ret = (basedigits[num % BASE]) + ret
        num = int(num / BASE)
    return ret
