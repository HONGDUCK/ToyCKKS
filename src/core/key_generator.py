from core.parameters import CKKSParameters
from lib.Ciphertext import Ciphertext 
from lib.Keys import SecretKey, RelinearizationKey

class KeyGenerator:
    def __init__(self, params: CKKSParameters):
        self.params = params
        self.slots = params.N // 2

    def gen_secret_key(self):
        cycloRing = self.params.rings[self.params.max_level]
        return SecretKey(self.params, cycloRing.sample_ternary())

    def gen_relinearization_key(self, secret_key: "SecretKey") -> "RelinearizationKey":
        aux_scale = 1 << self.params.log_aux_scale
        auxRing = self.params.auxRing
        s = secret_key.ringelem
        ss = s * s
        new_ring_s = auxRing.from_coeffs(ss.poly.coeffs)
        scaled = new_ring_s.scalarmul(aux_scale)

        S = auxRing.from_coeffs(s.poly._center_reduce())
        A = auxRing.random_uniform()
        E = auxRing.sample_Gaussian()

        B = A * S + scaled + E
        key = Ciphertext([A, B], aux_scale, self.params.max_level)

        return RelinearizationKey(self.params, key) 
