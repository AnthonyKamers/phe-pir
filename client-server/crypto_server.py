from utils import time_function


@time_function('sum_encrypted')
def sum_encrypted(array, encrypted_hot):
    encrypted_sum = None
    for i, ciphertext in enumerate(encrypted_hot):
        encrypted_sum = ciphertext * array[i].result if i == 0 else encrypted_sum + ciphertext * array[i].result
    return encrypted_sum
