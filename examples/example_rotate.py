import numpy as np
from lib.Plaintext import Plaintext
from core.cryptocontext import CryptoContext
from core.parameters import TOY

if __name__ == '__main__':
    cc = CryptoContext(TOY)
    slot_count = cc.slot_count
    max_level = cc.max_level

    shift = np.random.randint(0, slot_count) 
    msg = np.array([i for i in range(slot_count)])

    print("===== Plaintext rotation via automorphism =====")

    plaintext = cc.encode(msg)
    automorphismed = plaintext.ringelem.Auto(5 ** shift)
    rotated = Plaintext(automorphismed, plaintext.scale, plaintext.level)
    decoded = cc.decode(rotated)

    print("Ideal         : ", np.roll(msg, -shift))
    print("CKKS Rotation : ", decoded)
    print("Check         : ", np.allclose(np.roll(msg, -shift), decoded))
    

    print("===== Ciphertext rotation via key switching =====")
    secret_key = cc.keygen()

    rotation_key = cc.rotation_keygen(shift, secret_key)
    ciphertext = cc.encrypt(msg, secret_key)
    rotated = cc.rotate(ciphertext, rotation_key)
    result = cc.decrypt(rotated, secret_key)

    print("Ideal         : ", np.roll(msg, -shift))
    print("CKKS Rotation : ", result)
    print("Check         : ", np.allclose(np.roll(msg, -shift), result))

