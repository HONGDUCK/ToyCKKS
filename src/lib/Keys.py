from core.parameters import CKKSParameters
from lib.Polynomial import RingElem
from lib.Ciphertext import Ciphertext

class SecretKey:
    def __init__(self, params:CKKSParameters, ringelem: "RingElem"):
        self.params = params
        self.ringelem = ringelem

    # TODO: 같은 레벨이면 스킵
    def _fitting(self, level: int):
        cycloRing = self.params.rings[level]
        coeffs = self.ringelem.poly._center_reduce()
        self.ringelem = cycloRing.from_coeffs(coeffs)

    def _special_fitting(self):
        auxRing = self.params.auxRing
        coeffs = self.ringelem.poly._center_reduce()
        new_ringelem = auxRing.from_coeffs(coeffs)
        return SecretKey(self.params, new_ringelem)

class RelinearizationKey:
    def __init__(self, params:CKKSParameters, key: "Ciphertext"):
        self.params = params
        self.key = key

