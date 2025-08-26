import numpy as np
from core.key_generator import SecretKey
from lib.Ciphertext import Ciphertext
from lib.Plaintext import Plaintext

# encrypt, decrypt, keygen

class Encryptor:
    def __init__(self, params):
        self.params = params
        self.slots = params.N // 2

    # TODO: encode with an arbitrary level
    def encrypt(self, plaintext: "Plaintext", secret_key: "SecretKey", level: int = -1) -> "Ciphertext":
        if level == -1:
            level = self.params.max_level
        cycloRing = self.params.rings[level]
        pt = plaintext.ringelem
        s = secret_key.ringelem
        a = cycloRing.random_uniform()
        e = cycloRing.sample_Gaussian()
        b = a * s + pt + e
        return Ciphertext([a, b], self.params.scale, level)

    def decrypt(self, ciphertext: "Ciphertext", secret_key: "SecretKey") -> "Plaintext":
        if len(ciphertext.components) != 2:
            raise RuntimeError("Not allowed ciphertext format")
        a, b = ciphertext.components
        current_level = ciphertext.level
        secret_key._fitting(current_level) # Inplace
        s = secret_key.ringelem
        pt = b - a * s

        return Plaintext(pt, ciphertext.scale, current_level)


