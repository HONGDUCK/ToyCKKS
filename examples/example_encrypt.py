import numpy as np
from core.parameters import TOY
from core.encoder import Encoder
from core.encryptor import Encryptor
from core.key_generator import KeyGenerator

if __name__ == '__main__':
    encoder = Encoder(TOY)
    encryptor = Encryptor(TOY)
    keyGenerator = KeyGenerator(TOY)
    secret_key = keyGenerator.gen_secret_key()

    msg = np.array([4, 5, 3, 4, 4, 5, 3, 4], dtype=np.complex128) / 3

    plaintext = encoder.encode(msg)
    ciphertext = encryptor.encrypt(plaintext, secret_key)

    decrypted = encryptor.decrypt(ciphertext, secret_key)
    dec_msg = encoder.decode(decrypted)

    print(msg.real)
    print(dec_msg)
