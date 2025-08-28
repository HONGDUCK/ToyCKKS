import numpy as np
from core.parameters import TOY
from core.cryptocontext import CryptoContext

if __name__ == '__main__':
    cc = CryptoContext(TOY)
    slot_count = cc.slot_count
    max_level = cc.max_level

    secret_key = cc.keygen()
    msg1 = np.random.randint(-10, 10, size=slot_count) / 7
    msg2 = np.random.randint(-10, 10, size=slot_count) / 3

    ciphertext1 = cc.encrypt(msg1, secret_key)
    ciphertext2 = cc.encrypt(msg2, secret_key)

    print("===== Ciphertext-Ciphertext Addition =====")

    added = cc.add(ciphertext1, ciphertext2)
    result = cc.decrypt(added, secret_key)

    print("Ideal result  : ", msg1 + msg2)
    print("CKKS addition : ", result)
    print("Check : ", np.allclose(msg1 + msg2, result))

    print("===== Ciphertext-Scalar Addition =====")

    added = cc.add_scalar(ciphertext1, 7)
    result = cc.decrypt(added, secret_key)

    print("Ideal result  : ", msg1 + 7)
    print("CKKS addition : ", result)
    print("Check : ", np.allclose(msg1 + 7, result))

    print("===== Ciphertext-Messages Addition =====")

    msg3 = np.random.randint(-10, 10, size=slot_count) / 5
    added = cc.add_messages(ciphertext1, msg3)
    result = cc.decrypt(added, secret_key)

    print("Ideal result  : ", msg1 + msg3)
    print("CKKS addition : ", result)
    print("Check : ", np.allclose(msg1 + msg3, result))
