import numpy as np
from core.parameters import TOY
from core.cryptocontext import CryptoContext

if __name__ == '__main__':
    cc = CryptoContext(TOY)
    slot_count = cc.slot_count
    max_level = cc.max_level

    msg1 = np.random.randint(-10, 10, size=slot_count) / 7
    msg2 = np.random.randint(-10, 10, size=slot_count) / 3

    secret_key = cc.keygen()
    ciphertext1 = cc.encrypt(msg1, secret_key)
    ciphertext2 = cc.encrypt(msg2, secret_key)

    added = cc.add(ciphertext1, ciphertext2)

    result = cc.decrypt(added, secret_key)

    print("Ideal result  : ", msg1 + msg2)
    print("CKKS addition : ", result)
    print("Check : ", np.allclose(msg1 + msg2, result))
