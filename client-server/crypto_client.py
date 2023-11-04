from damgard_jurik import keygen as damgard_jurik_keygen
from phe.paillier import generate_paillier_keypair as paillier_keygen

from okamoto_uchiyama.okamoto_uchiyama import generate_okamoto_uchiyama as okamoto_uchiyama_keygen
from utils import time_function

DAMGARD_JURIK_BIT_SIZE = 64
DEFAULT_BIT_SIZE = 512

schemes = ['okamoto-uchiyama-self', 'damgard-jurik', 'paillier',]

@time_function('keygen')
def generate_keypair(scheme: str):
    if scheme in schemes:
        match scheme:
            case 'paillier':
                return paillier_keygen(n_length=DEFAULT_BIT_SIZE)
            case 'okamoto-uchiyama-self':
                return okamoto_uchiyama_keygen(DEFAULT_BIT_SIZE)
            case 'damgard-jurik':
                return damgard_jurik_keygen(DAMGARD_JURIK_BIT_SIZE)
    else:
        raise ValueError('Invalid scheme')


def plain_hot(index: int, length: int):
    return [1 if i == index else 0 for i in range(length)]


@time_function('encrypt_vector')
def encrypt_hot(hot_array, public):
    return [public.encrypt(number) for number in hot_array]
