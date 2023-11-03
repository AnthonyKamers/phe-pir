from damgard_jurik import keygen as damgard_jurik_keygen
from phe.paillier import generate_paillier_keypair as paillier_keygen

from okamoto_uchiyama.okamoto_uchiyama import generate_okamoto_uchiyama as okamoto_uchiyama_keygen
from utils import time_function

map_scheme_algorithm = {
    'okamoto-uchiyama': okamoto_uchiyama_keygen,
    'damgard-jurik': damgard_jurik_keygen,
    'paillier': paillier_keygen,
}


@time_function('keygen')
def generate_keypair(scheme: str):
    if scheme in map_scheme_algorithm:
        return map_scheme_algorithm[scheme]()
    else:
        raise ValueError('Invalid scheme')


def plain_hot(index: int, length: int):
    return [1 if i == index else 0 for i in range(length)]


@time_function('encrypt_vector')
def encrypt_hot(hot_array, public):
    return [public.encrypt(number) for number in hot_array]
