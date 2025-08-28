import numpy as np
from core.parameters import CKKSParameters
from core.key_generator import KeyGenerator
from core.encoder import Encoder
from core.encryptor import Encryptor
from core.operator import Operator
from lib.Keys import SecretKey
from lib.Ciphertext import Ciphertext
from lib.Plaintext import Plaintext
from utils.rejections import (_valid_scalar, _valid_array_dtype,
                              _check_msg_length, _check_ciphertext_components)
from utils.checker import (_is_scalar_integer)

class CryptoContext:
    def __init__(self, params: "CKKSParameters"):
        self.params = params
        self.keyGenerator = KeyGenerator(params)
        self.encoder = Encoder(params)
        self.encryptor = Encryptor(params)
        self.operator = Operator(params)

    def keygen(self):
        return self.keyGenerator.gen_secret_key()

    def encode(self, msg: np.ndarray, level: int = -1):
        if level == -1:
            level = self.params.max_level
        encoded = self.encoder.encode(msg, level)
        return encoded

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

    def add(self, ct1: "Ciphertext", ct2: "Ciphertext") -> "Ciphertext":
        return self.operator.add(ct1, ct2)

    def add_plain(self, ct: "Ciphertext", pt: "Plaintext") -> "Ciphertext":
        return self.operator.add_plain(ct, pt)

    # 우선 정수, 실수만 허용
    def add_scalar(self, ct: "Ciphertext", scalar: np.int64|np.float64|int|float) -> "Ciphertext":
        _valid_scalar(scalar)
        slot_count = self.slot_count
        ct_level = ct.level
        messages = np.repeat(scalar, slot_count)
        plaintext = self.encoder.encode(messages, ct_level)
        return self.operator.add_plain(ct, plaintext)

    # 우선 정수, 실수만 허용
    def add_messages(self, ct: "Ciphertext", messages: np.ndarray) -> "Ciphertext":
        slot_count = self.slot_count
        _valid_array_dtype(messages)
        _check_msg_length(messages, slot_count)
        ct_level = ct.level
        plaintext = self.encoder.encode(messages, ct_level)
        return self.operator.add_plain(ct, plaintext)

    def mul_plain(self, ct: "Ciphertext", pt: "Plaintext") -> "Ciphertext":
        return self.operator.mul_plain(ct, pt)

    def mul_scalar(self, ct: "Ciphertext", scalar: np.int64|np.float64|int|float) -> "Ciphertext":
        _check_ciphertext_components(ct)
        if _is_scalar_integer(scalar): # No need to encode = no need to consume level
            a, b = ct.components
            new_a = a.scalarmul(int(scalar))
            new_b = b.scalarmul(int(scalar))
            return Ciphertext([new_a, new_b], ct.scale, ct.level)
        else:
            slot_count = self.params.slot_count
            message = np.repeat(scalar, slot_count)
            plaintext = self.encoder.encode(message)
            return self.operator.mul_plain(ct, plaintext)

    def mul_messages(self, ct: "Ciphertext", messages: np.ndarray):
        slot_count = self.params.slot_count
        _valid_array_dtype(messages)
        _check_msg_length(messages, slot_count)
        ct_level = ct.level
        plaintext = self.encoder.encode(messages, ct_level)
        return self.operator.mul_plain(ct, plaintext)

    @property
    def slot_count(self):
        return self.params.slot_count

    @property
    def max_level(self):
        return self.params.max_level
