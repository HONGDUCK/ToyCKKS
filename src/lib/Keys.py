from core.parameters import CKKSParameters
from lib.Polynomial import RingElem
from lib.Ciphertext import Ciphertext

class SecretKey:
    def __init__(self, params:CKKSParameters, ringelem: "RingElem"):
        self.params = params
        self.ringelem = ringelem

    def _fitting(self, level: int) -> "SecretKey":
        cycloRing = self.params.rings[level]
        coeffs = self.ringelem.poly._center_reduce()
        ringelem = cycloRing.from_coeffs(coeffs)
        return SecretKey(self.params, ringelem)

class RelinearizationKey:
    def __init__(self, params:CKKSParameters, key: "Ciphertext"):
        self.params = params
        self.key = key

class RotationKey:
    def __init__(self, params: CKKSParameters, key: "Ciphertext", shift: int):
        self.params = params
        self.shift = shift
        self.key = key
