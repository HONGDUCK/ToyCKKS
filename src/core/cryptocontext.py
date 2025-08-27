import numpy as np
from core.parameters import CKKSParameters
from core.key_generator import KeyGenerator
from core.encoder import Encoder
from core.encryptor import Encryptor
from core.operator import Operator
from lib.Keys import SecretKey
from lib.Ciphertext import Ciphertext
from lib.Plaintext import Plaintext

class CryptoContext:
    def __init__(self, params: "CKKSParameters"):
        self.params = params
        self.keyGenerator = KeyGenerator(params)
        self.encoder = Encoder(params)
        self.encryptor = Encryptor(params)
        self.operator = Operator(params)

    def keygen(self):
        return self.keyGenerator.gen_secret_key()

    def encrypt(self, msg: np.ndarray, secret_key: "SecretKey", level: int = -1):
        if level == -1:
            level = self.params.max_level
        encoded = self.encoder.encode(msg, level)
        ciphertext = self.encryptor.encrypt(encoded, secret_key)
        return ciphertext

    def decrypt(self, ct: "Ciphertext", secret_key: "SecretKey"):
        plaintext = self.encryptor.decrypt(ct, secret_key)
        message = self.encoder.decode(plaintext)
        return message

    # TODO: add scalar, add vector 
    def add(self, ct1: "Ciphertext", ct2: "Ciphertext"):
        return self.operator.add(ct1, ct2)

    def add_plain(self, ct: "Ciphertext", pt: "Plaintext"):
        return self.operator.add_plain(ct, pt)

    @property
    def slot_count(self):
        return self.params.slot_count

    @property
    def max_level(self):
        return self.params.max_level
