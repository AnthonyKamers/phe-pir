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


map_private_key_title = {
    'paillier': 'p,q',
    'damgard-jurik': 'Four delta values',
    'okamoto-uchiyama': 'p,q'
}


def show_title_private_key():
    return map_private_key_title[session['scheme']]


def show_private_key():
    scheme = session['scheme']
    private = session['private']
    match scheme:
        case 'paillier' | 'okamoto-uchiyama':
            return f'{private.p}|{private.q}'
        case 'damgard-jurik':
            return f'{private.inv_four_delta_squared}'
        case _:
            return 'Undefined'


def show_encrypted_value(encrypted):
    scheme = session['scheme']
    match scheme:
        case 'paillier':
            return encrypted._EncryptedNumber__ciphertext
        case 'damgard-jurik':
            return encrypted.value
        case 'okamoto-uchiyama':
            return encrypted.ciphertext
        case _:
            return 'Undefined'
