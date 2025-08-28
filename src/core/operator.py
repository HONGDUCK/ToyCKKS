from __future__ import print_function
from lib.Ciphertext import Ciphertext
from lib.Plaintext import Plaintext
from core.parameters import CKKSParameters
from lib.Polynomial import RingElem
from utils.rejections import (_check_ciphertext_components,
                              _check_components,
                              _is_small_level_ct,
                              _is_small_level_pt,
                              _is_level_zero)

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
        p = level_downed_pt.ringelem
        added_b = b + p
        return Ciphertext([a, added_b], self.params.scale, ct_level)

    def mul(self, ct1: Ciphertext, ct2: Ciphertext) -> Ciphertext:
        return NotImplemented

    def mul_plain(self, ct: Ciphertext, pt: Plaintext) -> "Ciphertext":
        _check_ciphertext_components(ct)
        _is_level_zero(ct)
        ct_level = ct.level
        level_downed_pt = self._level_down_pt(pt, ct_level)
        p = level_downed_pt.ringelem
        a, b = ct.components
        multiplied_a = a * p
        multiplied_b = b * p

        downed_level = ct_level - 1
        rescaled_a, rescaled_b = self.rescale([multiplied_a, multiplied_b], downed_level)

        return Ciphertext([rescaled_a, rescaled_b], self.params.scale, downed_level)

    def rescale(self, components: list["RingElem"], downed_level: int) -> list["RingElem"]:
        _check_components(components)
        cycloRing = self.params.rings[downed_level]
        log_scale = self.params.log_scale

        a, b = components
        coeffs_a, coeffs_b = a.poly.coeffs, b.poly.coeffs
        for i in range(self.params.N):
            coeffs_a[i] = div_round_power2(coeffs_a[i], log_scale)
            coeffs_b[i] = div_round_power2(coeffs_b[i], log_scale)

        new_a = cycloRing.from_coeffs(coeffs_a)
        new_b = cycloRing.from_coeffs(coeffs_b)

        return [new_a, new_b]

def div_round_power2(a, shift):
    # arr: np.ndarray of ints mod q (0..q-1)
    # 반올림 나눗셈: floor((x + 2^(shift-1)) / 2^shift)
    return (a + (1 << (shift-1))) >> shift
