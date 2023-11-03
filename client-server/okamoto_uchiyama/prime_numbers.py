from random import randint, getrandbits


# sources:
# https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
# https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/
def miller_rabin(n, k=128):
    if n <= 3:
        return True

    if n % 2 == 0:
        return False

    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = randint(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# source:
# https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=1024):
    p = 4

    while not miller_rabin(p, 128):
        p = generate_prime_candidate(length)
    return p
