# tests/test_polynomial_numpy_compare.py
import numpy as np
import pytest

from lib.Polynomial import SingleMod, CyclotomicRing

# --------- NumPy 쪽 헬퍼들 (상승차수 계수: a[0] + a[1] X + ... ) ---------

def mod_q(a, q):
    return np.mod(np.array(a, dtype=int), q)

def reduce_mod_xn1(poly, N, q):
    """
    poly: ascending power coefficients (len may be > N)
    Reduce modulo (X^N + 1) and q.
    Relation: X^N ≡ -1  =>  X^{N+m} ≡ -X^m
    """
    coeffs = np.array(poly, dtype=int)
    if len(coeffs) > N:
        # 누적해서 낮은 차수로 흘려보내기
        for i in range(N, len(coeffs)):
            coeffs[i - N] = (coeffs[i - N] - coeffs[i])  # '-=' because X^N ≡ -1
        coeffs = coeffs[:N]
    else:
        coeffs = np.pad(coeffs, (0, N - len(coeffs)), constant_values=0)
    return mod_q(coeffs, q)

def mul_cyclotomic(poly1, poly2, N, q):
    """ (poly1 * poly2) mod (X^N + 1, q) """
    conv = np.convolve(np.array(poly1, dtype=int), np.array(poly2, dtype=int))
    return reduce_mod_xn1(conv, N, q)

def automorphism_numpy(poly, k, N, q):
    """
    a(X) -> a(X^k) in Z_q[X]/(X^N + 1)
    poly: ascending coefficients (len == N)
    """
    k = k % (2 * N)
    res = np.zeros(N, dtype=int)

    for i, ai in enumerate(np.array(poly, dtype=int)):
        if ai == 0:
            continue
        e = (i * k) % (2 * N)
        if e >= N:
            idx = e - N
            res[idx] -= ai  # sign flip due to X^N = -1
        else:
            res[e] += ai

    return np.mod(res, q)


# --------- PyTest ---------

@pytest.mark.parametrize("N,q,k1,k2", [
    (8, 64, 3, 5),
    (16, 257, 3, 5),
    (32, 12289, 3, 5),
])
def test_ring_vs_numpy(N, q, k1, k2):
    R = CyclotomicRing.create(N, SingleMod(q))

    # 여러 번 랜덤 검증
    for _ in range(10):
        a = R.random_uniform()  # Ring element (len N)
        b = R.random_uniform()

        a_np = np.array(a.tolist(), dtype=int)
        b_np = np.array(b.tolist(), dtype=int)

        # --- 덧셈 ---
        ours_add = (a + b).tolist()
        numpy_add = mod_q(a_np + b_np, q)
        assert np.array_equal(np.array(ours_add, dtype=int), numpy_add), "Addition mismatch"

        # --- 곱셈 ---
        ours_mul = (a * b).tolist()
        numpy_mul = mul_cyclotomic(a_np, b_np, N, q)
        assert np.array_equal(np.array(ours_mul, dtype=int), numpy_mul), "Multiplication mismatch"

        # --- 자동동형 X->X^k1 ---
        ours_auto1 = a.Auto(k1).tolist()
        numpy_auto1 = automorphism_numpy(a_np, k1, N, q)
        assert np.array_equal(np.array(ours_auto1, dtype=int), numpy_auto1), f"Automorphism k={k1} mismatch"

        # --- 자동동형 X->X^k2 ---
        ours_auto2 = b.Auto(k2).tolist()
        numpy_auto2 = automorphism_numpy(b_np, k2, N, q)
        assert np.array_equal(np.array(ours_auto2, dtype=int), numpy_auto2), f"Automorphism k={k2} mismatch"

