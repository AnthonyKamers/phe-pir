from math import gcd
from random import randint

from .math_utils import modular_inverse
from .prime_numbers import generate_prime_number


# sources:
# https://link.springer.com/content/pdf/10.1007/BFb0054135.pdf - Original cryptosystem
# https://link.springer.com/book/10.1007/978-3-030-87629-6 - Book followed
# https://github.com/mounikapratapa/Okamoto-Uchiyama-implementation - Some implementation
class AbstractPublicKey:
    def __init__(self, public_key: "PublicKeyOkamotoUchiyama"):
        self.public_key = public_key

    @staticmethod
    def check_public_key(val1: "AbstractPublicKey", val2: "AbstractPublicKey"):
        if val1.public_key != val2.public_key:
            raise Exception(f"The public key is not the same")


class EncryptedOkamotoUchiyama(AbstractPublicKey):
    def __init__(self, ciphertext: int, public_key: "PublicKeyOkamotoUchiyama"):
        super().__init__(public_key)
        self.ciphertext = ciphertext

    # Sum of ciphertexts
    def __add__(self, val2: "EncryptedOkamotoUchiyama"):
        if not isinstance(val2, EncryptedOkamotoUchiyama):
            raise Exception("You can only sum ciphertexts")
        AbstractPublicKey.check_public_key(self, val2)
        return EncryptedOkamotoUchiyama(self.ciphertext * val2.ciphertext, self.public_key)

    # multiplication by scalar
    def __mul__(self, val2: int):
        if not isinstance(val2, int):
            raise Exception("You can only multiply a ciphertext with an integer scalar")
        return EncryptedOkamotoUchiyama(pow(self.ciphertext, val2, self.public_key.n), self.public_key)


class PublicKeyOkamotoUchiyama:
    def __init__(self, n: int, g: int, h: int, k: int):
        self.n = n
        self.g = g
        self.h = h
        self.k = k

    def encrypt(self, m: int) -> EncryptedOkamotoUchiyama:
        if m < 0 or m > 2 ** (self.k - 1):
            raise Exception(f"The message must be between 0 and 2**{self.k - 1}")

        r = randint(1, self.n)
        ciphertext = pow(self.g, m + (self.n * r), self.n)
        return EncryptedOkamotoUchiyama(ciphertext, self)


class PrivateKeyOkamotoUchiyama(AbstractPublicKey):
    def __init__(self, p: int, q: int, public_key: PublicKeyOkamotoUchiyama):
        super().__init__(public_key)
        self.p = p
        self.p_square = p * p
        self.q = q

    def decrypt(self, ciphertext: EncryptedOkamotoUchiyama):
        AbstractPublicKey.check_public_key(self, ciphertext)

        g_p = modular_inverse(self.discrete_logarithm(self.public_key.g), self.p)
        c_p = self.discrete_logarithm(ciphertext.ciphertext)
        return (c_p * g_p) % self.p

    def discrete_logarithm(self, c: int):
        z = pow(c, self.p - 1, self.p_square)
        return self.L(z)

    def L(self, z):
        return (z - 1) // self.p


def generate_okamoto_uchiyama(k_bits: int = 512) -> tuple[PublicKeyOkamotoUchiyama, PrivateKeyOkamotoUchiyama]:
    while True:
        p = generate_prime_number(k_bits)
        q = generate_prime_number(k_bits)

        if gcd(p, q - 1) == 1 and gcd(p - 1, q) == 1:
            break

    p_square = p * p
    n = p_square * q
    while True:
        aux = randint(0, n)
        g = pow(aux, p - 1, p_square)
        if g != 1:
            break

    h = pow(g, n, n)
    public_key = PublicKeyOkamotoUchiyama(n, g, h, k_bits)
    private_key = PrivateKeyOkamotoUchiyama(p, q, public_key)
    return public_key, private_key


if __name__ == "__main__":
    number1 = 5
    number2 = 7
    scalar = 9

    public, private = generate_okamoto_uchiyama()

    encryptNumber1 = public.encrypt(number1)
    encryptNumber2 = public.encrypt(number2)
    sum_ciphertext = encryptNumber1 + encryptNumber2
    multiplication_scalar = encryptNumber1 * scalar

    assert (private.decrypt(sum_ciphertext) == number1 + number2)
    assert (private.decrypt(multiplication_scalar) == number1 * scalar)
