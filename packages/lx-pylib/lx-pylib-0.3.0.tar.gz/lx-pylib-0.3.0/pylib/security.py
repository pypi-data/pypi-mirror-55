# -*- coding: utf-8 -*-

import hmac
from random import SystemRandom

from ._compat import range_type, text_type

SALT_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

_sys_rng = SystemRandom()


def gen_salt(length):
    """Generate a random string of SALT_CHARS with specified ``length``."""
    if length <= 0:
        raise ValueError('Salt length must be positive')
    return ''.join(_sys_rng.choice(SALT_CHARS) for _ in range_type(length))


def password_hash(password, salt):
    if isinstance(password, text_type):
        password = password.encode('utf-8')
    if isinstance(salt, text_type):
        salt = salt.encode('utf-8')
    return hmac.new(salt, password).hexdigest()
