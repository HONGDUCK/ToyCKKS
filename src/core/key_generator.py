from core.parameters import CKKSParameters
from lib.Keys import SecretKey

class KeyGenerator:
    def __init__(self, params: CKKSParameters):
        self.params = params
        self.slots = params.N // 2

    def gen_secret_key(self):
        cycloRing = self.params.rings[self.params.max_level]
        return SecretKey(self.params, cycloRing.sample_ternary())

