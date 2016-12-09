import random
import string

import shortuuid

shortuuid.set_alphabet(string.ascii_uppercase + string.digits)


def get_random_string(length):
    # 0123456789ABCDEFGHJKLMNPQRSTUVWXYZ
    return ''.join([random.choice(string.ascii_uppercase + string.digits)
                    for n in range(length)])


def get_uuid(length):
    return shortuuid.uuid()[:length]


def format_url(url):
    return url
