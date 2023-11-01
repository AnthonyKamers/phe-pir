from damgard_jurik import keygen
from phe import paillier

from utils import time_function


@time_function('keygen')
def generate_keypair(scheme: str):
    if scheme == 'paillier':
        return paillier.generate_paillier_keypair()
    elif scheme == 'damgard-jurik':
        return keygen()
    else:
        raise ValueError('Invalid scheme')


def plain_hot(index: int, length: int):
    return [1 if i == index else 0 for i in range(length)]


@time_function('encrypt_vector')
def encrypt_hot(hot_array, public):
    return [public.encrypt(number) for number in hot_array]
