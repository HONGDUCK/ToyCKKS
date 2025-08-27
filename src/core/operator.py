from lib.Ciphertext import Ciphertext
from lib.Plaintext import Plaintext
from core.parameters import CKKSParameters
from utils.rejections import (_check_ciphertext_components,
                              _is_small_level_ct,
                              _is_small_level_pt)

class Operator:
    def __init__(self, params: "CKKSParameters"):
        self.params= params

    # --- Utils ---
    def _level_down_ct(self, ct: Ciphertext, target_level: int) -> Ciphertext:
        _check_ciphertext_components(ct)
        _is_small_level_ct(ct, target_level)

        if ct.level == target_level:
            return ct

        cycloRing = self.params.rings[target_level]
        a, b = ct.components

        coeffs_a = a.poly._center_reduce()
        coeffs_b = b.poly._center_reduce()

        level_downed_a = cycloRing.from_coeffs(coeffs_a)
        level_downed_b = cycloRing.from_coeffs(coeffs_b)

        return Ciphertext([level_downed_a, level_downed_b],
                          self.params.scale, target_level)

    def _level_down_pt(self, pt: Plaintext, target_level: int) -> Plaintext:
        _is_small_level_pt(pt, target_level)
        if pt.level == target_level:
            return pt

        cycloRing = self.params.rings[target_level]
        coeffs = pt.ringelem.poly._center_reduce()
        level_downed = cycloRing.from_coeffs(coeffs)
        return Plaintext(level_downed, self.params.scale, target_level)

    # --- Operations ---
    def add(self, ct1: Ciphertext, ct2: Ciphertext) -> Ciphertext:
        _check_ciphertext_components(ct1)
        _check_ciphertext_components(ct2)

        min_level = min(ct1.level, ct2.level)
        level_downed1 = self._level_down_ct(ct1, min_level)
        level_downed2 = self._level_down_ct(ct2, min_level)

        a1, b1 = level_downed1.components
        a2, b2 = level_downed2.components

        added_a = a1 + a2
        added_b = b1 + b2

        return Ciphertext([added_a, added_b], self.params.scale, min_level)

    def add_plain(self, ct: Ciphertext, pt: Plaintext) -> Ciphertext:
        _check_ciphertext_components(ct)
        ct_level = ct.level
        level_downed_pt = self._level_down_pt(pt, ct_level)
        a, b = ct.components
        poly = level_downed_pt.ringelem
        added_b = b + poly
        return Ciphertext([a, added_b], self.params.scale, ct_level)

    def mul_plain(self, ct: Ciphertext, pt: Plaintext) -> Ciphertext:
        return NotImplemented

    def mul(self, ct1: Ciphertext, ct2: Ciphertext) -> Ciphertext:
        return NotImplemented

    def rescale(self, ct: Ciphertext) -> Ciphertext:
        return NotImplemented

