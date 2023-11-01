import string
import time
from random import SystemRandom

from flask import session


def private_key_sessions():
    return ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))


# calculate function time and put into session with 'argument' key
# https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
# https://stackoverflow.com/questions/5929107/decorators-with-parameters
def time_function(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            ret = function(*args, **kwargs)
            time_elapsed = time.time() - start_time

            # put into session
            session[f'time_{argument}'] = round(time_elapsed, 4)
            return ret

        return wrapper

    return decorator


def show_title_private_key():
    scheme = session['scheme']
    if scheme == 'paillier':
        return 'p,q'
    elif scheme == 'damgard-jurik':
        return 'Four delta values'


def show_private_key():
    scheme = session['scheme']
    private = session['private']
    if scheme == 'paillier':
        return f'{private.p}|{private.q}'
    elif scheme == 'damgard-jurik':
        return f'{private.inv_four_delta_squared}'


def show_encrypted_value(encrypted):
    scheme = session['scheme']
    if scheme == 'paillier':
        return encrypted._EncryptedNumber__ciphertext
    elif scheme == 'damgard-jurik':
        return encrypted.value
