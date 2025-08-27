import numpy as np
from core.key_generator import SecretKey
from lib.Ciphertext import Ciphertext
from lib.Plaintext import Plaintext
from utils.rejections import (_check_ciphertext_components)

# encrypt, decrypt, keygen

class Encryptor:
    def __init__(self, params):
        self.params = params
        self.slots = params.N // 2

    # TODO: encode with an arbitrary level
    def encrypt(self, plaintext: "Plaintext", secret_key: "SecretKey") -> "Ciphertext":
        level = plaintext.level
        secret_key._fitting(level)
        cycloRing = self.params.rings[level]
        pt = plaintext.ringelem
        s = secret_key.ringelem
        a = cycloRing.random_uniform()
        e = cycloRing.sample_Gaussian()
        b = a * s + pt + e
        return Ciphertext([a, b], self.params.scale, level)

    def decrypt(self, ciphertext: "Ciphertext", secret_key: "SecretKey") -> "Plaintext":
        _check_ciphertext_components(ciphertext)
        a, b = ciphertext.components
        current_level = ciphertext.level
        secret_key._fitting(current_level)
        s = secret_key.ringelem
        pt = b - a * s

        return Plaintext(pt, ciphertext.scale, current_level)


