from lib.Ciphertext import Ciphertext
from lib.Plaintext import Plaintext
from lib.Polynomial import RingElem
from lib.Keys import RelinearizationKey, RotationKey
from core.parameters import CKKSParameters
from utils.rejections import (_check_ciphertext_components,
                              _check_components,
                              _check_triple_components,
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

    # --- Additions ---
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

    # --- Multiplications ---
    def mul(self, ct1: "Ciphertext", ct2: "Ciphertext",
            relinearization_key: "RelinearizationKey") -> "Ciphertext":
        min_level = min(ct1.level, ct2.level)
        level_downed_ct1 = self._level_down_ct(ct1, min_level)
        level_downed_ct2 = self._level_down_ct(ct2, min_level)

        a1, b1 = level_downed_ct1.components
        a2, b2 = level_downed_ct2.components

        aa = a1 * a2
        abba = a1 * b2 + b1 * a2
        bb = b1 * b2

        relin_a, relin_b = self.relinearize([aa, abba, bb], relinearization_key, min_level)
        rescaled_a, rescaled_b = self.rescale([relin_a, relin_b], min_level - 1)

        return Ciphertext([rescaled_a, rescaled_b], self.params.scale, min_level-1)

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

    # --- Rotation ---
    def rotation(self, ciphertext: "Ciphertext", rotation_key: "RotationKey") -> "Ciphertext":
        _check_ciphertext_components(ciphertext)
        shift = rotation_key.shift
        current_level = ciphertext.level

        a,b = ciphertext.components
        auto_a = a.Auto(5 ** shift)
        auto_b = b.Auto(5 ** shift)

        [switched_a, switched_b] = self.keyswitch([auto_a, auto_b], rotation_key, current_level)

        return Ciphertext([switched_a, switched_b], self.params.scale, current_level)

    # --- Key Switchings ---
    def relinearize(self, components: list["RingElem"], relinearization_key: "RelinearizationKey",
                    current_level: int) -> list["RingElem"]:
        _check_triple_components(components)
        auxRing = self.params.auxRing
        cycloRing = self.params.rings[current_level]
        log_aux_scale = self.params.log_aux_scale

        aa, abba, bb = components
        key_a, key_b = relinearization_key.key.components

        tmp_aa = auxRing.from_coeffs(aa.poly.coeffs)

        re_a = tmp_aa * key_a
        re_b = tmp_aa * key_b

        coeffs_a, coeffs_b =  re_a.poly.coeffs, re_b.poly.coeffs
        for i in range(self.params.N):
            coeffs_a[i] = div_round_power2(coeffs_a[i], log_aux_scale)
            coeffs_b[i] = div_round_power2(coeffs_b[i], log_aux_scale)

        new_a = cycloRing.from_coeffs(coeffs_a)
        new_b = cycloRing.from_coeffs(coeffs_b)

        return [abba + new_a, bb + new_b]

    def keyswitch(self, components: list["RingElem"], rotation_key: "RotationKey",
                  current_level: int) -> list["RingElem"]:
        _check_components(components)
        auxRing = self.params.auxRing
        cycloRing = self.params.rings[current_level]
        log_aux_scale = self.params.log_aux_scale

        auto_a, auto_b = components
        key_a, key_b = rotation_key.key.components

        tmp_aa = auxRing.from_coeffs(auto_a.poly.coeffs)

        switched_a = tmp_aa * key_a
        switched_b = tmp_aa * key_b

        coeffs_a, coeffs_b =  switched_a.poly.coeffs, switched_b.poly.coeffs
        for i in range(self.params.N):
            coeffs_a[i] = div_round_power2(coeffs_a[i], log_aux_scale)
            coeffs_b[i] = div_round_power2(coeffs_b[i], log_aux_scale)

        new_a = cycloRing.from_coeffs(coeffs_a)
        new_b = cycloRing.from_coeffs(coeffs_b)

        return [new_a, auto_b + new_b]

def div_round_power2(a, shift):
    # arr: np.ndarray of ints mod q (0..q-1)
    # 반올림 나눗셈: floor((x + 2^(shift-1)) / 2^shift)
    return (a + (1 << (shift-1))) >> shift
