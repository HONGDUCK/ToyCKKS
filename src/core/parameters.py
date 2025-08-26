import numpy as np
from lib.Polynomial import CyclotomicRing, SingleMod

# q0 = 50bits 으로 가정
def GenCyclotomicRings(N, log_scale, max_level):
    rings = []
    LOG = 50
    for _ in range(max_level + 1):
        rings.append(CyclotomicRing.create(N, SingleMod(1 << LOG)))
        LOG += log_scale
    return rings

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

        # Cyclotomic ring 초기화 
        self.rings = GenCyclotomicRings(self.N, self.log_scale, self.max_level)

TOY = CKKSParameters(16, 250, 40, 3.2) # max_level = 5

