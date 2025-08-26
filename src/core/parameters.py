import numpy as np
from lib.Polynomial import CyclotomicRing, SingleMod

# q0 = 50bits 으로 가정
def GenLogModulusTable(log_scale, max_level):
    log_modulus_table = []
    log_bottom_q = 50
    for _ in range(max_level + 1):
        log_modulus_table.append(log_bottom_q)
        log_bottom_q += log_scale

    return np.array(log_modulus_table, dtype=int)

# q0 = 50bits 으로 가정
# TODO: bottom_modulus 정의
class CKKSParameters:
    def __init__(self, N: int, log_q: int, log_scale: int, sigma: float = 3.2):
        self.N = N
        self.q = 1 << log_q
        self.log_q = log_q
        self.scale = 1 << log_scale
        self.log_scale = log_scale
        self.sigma = sigma
        self.max_level = (log_q - 50) // log_scale
        self.log_modulus_table = GenLogModulusTable(log_scale, self.max_level)

        # Cyclotomic ring 초기화
        self.ring = CyclotomicRing.create(N, SingleMod(self.q))

TOY = CKKSParameters(16, 250, 40, 3.2) # max_level = 5

