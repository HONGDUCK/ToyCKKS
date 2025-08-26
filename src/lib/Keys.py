from core.parameters import CKKSParameters
from lib.Polynomial import RingElem

class SecretKey:
    def __init__(self, params:CKKSParameters, ringelem: "RingElem"):
        self.params = params
        self.ringelem = ringelem

    # TODO: 같은 레벨이면 스킵
    def _fitting(self, level: int):
        cycloRing = self.params.rings[level]
        coeffs = self.ringelem.poly._center_reduce()
        self.ringelem = cycloRing.from_coeffs(coeffs)


