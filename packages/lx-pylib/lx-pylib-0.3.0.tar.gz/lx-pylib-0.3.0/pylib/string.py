# -*- coding: utf-8 -*-

import string
import random
import re


def random_string(length=8, allowed_chars=None):
    if allowed_chars is None:
        allowed_chars = string.ascii_letters + string.digits
    return ''.join(random.sample(allowed_chars, length))


def str_to_tags(s):
    return [v for v in re.split(r'[ ,;|]+', s)]


def display_width(s):
    pattern = u"[\u4e00-\u9fa5]+"
    searched = re.findall(pattern, s)
    ch_len = 0

    if searched:
        for x in searched:
            ch_len += len(x) * 2

    strip_ch_len = len(re.sub(pattern, u'', s))

    return ch_len + strip_ch_len
