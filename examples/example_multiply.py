import numpy as np
from numpy._core.multiarray import scalar
from core.parameters import TOY
from core.cryptocontext import CryptoContext

if __name__ == '__main__':
    cc = CryptoContext(TOY)
    slot_count = cc.slot_count
    secret_key = cc.keygen()

    msg1 = np.random.randint(-10, 10, size=slot_count) / 3
    msg2 = np.random.randint(-10, 10, size=slot_count) / 3

    ciphertext = cc.encrypt(msg1, secret_key)

    print("===== Ciphertext * Messages =====")

    multiplied = cc.mul_messages(ciphertext, msg2)
    result = cc.decrypt(multiplied, secret_key)

    print("Ideal result        : ", msg1 * msg2)
    print("CKKS multiplication : ", result)
    print("Consumed level      : ", ciphertext.level - multiplied.level)
    print("Check : ", np.allclose(msg1 * msg2, result))

    print("===== Ciphertext * Scalar(double) =====")

    scalar = np.random.rand()

    multiplied = cc.mul_scalar(ciphertext, scalar)
    result = cc.decrypt(multiplied, secret_key)

    print("Ideal result        : ", msg1 * scalar)
    print("CKKS multiplication : ", result)
    print("Consumed level      : ", ciphertext.level - multiplied.level)
    print("Check : ", np.allclose(msg1 * scalar, result))

    print("===== Ciphertext * Scalar(int) =====")

    scalar = np.random.randint(-10, 10)

    multiplied = cc.mul_scalar(ciphertext, scalar)
    result = cc.decrypt(multiplied, secret_key)

    print("Ideal result        : ", msg1 * scalar)
    print("CKKS multiplication : ", result)
    print("Consumed level      : ", ciphertext.level - multiplied.level)
    print("Check : ", np.allclose(msg1 * scalar, result))

