import numpy as np
from numpy.polynomial import Polynomial as P
from lib.Polynomial import SingleMod, CyclotomicRing

def poly_compose_power(a, k):
    N = len(a)
    # 결과 다항식은 최대 (N-1)*k 차수까지 나올 수 있음
    res = np.zeros((N - 1) * k + 1, dtype=object)
    for i, ai in enumerate(a):
        if ai != 0:
            res[i * k] += ai
    return res

if __name__ == "__main__":
    N = 8
    q = 64
    R = CyclotomicRing.create(N, SingleMod(q))

    a = R.random_uniform()
    b = R.random_uniform()


    print("Polaynomial1                    : ", a.tolist())
    print("Polaynomial2                    : ", b.tolist())

    print("====== Ours ======")

    c = a + b
    d = a * b

    e = a.Auto(3)
    f = b.Auto(5)

    print("Polynomial addition             : ", c.tolist())
    print("Polynomial multiplication       : ", d.tolist())
    print("Polynomial1 automorphism with 3 : ", e.tolist())
    print("Polynomial2 automorphism with 5 : ", f.tolist())

    print("====== Numpy ======")
    poly1 = np.array(a.tolist(), dtype=int)
    poly2 = np.array(b.tolist(), dtype=int)

    poly_add = np.mod(poly1 + poly2, q)

    divisor     = np.zeros(N+1) # (X^N+1)
    divisor[0]  = divisor[-1] = 1

    poly_mul      = np.polymul(poly1[::-1], poly2[::-1])
    _, remainder  = np.polydiv(poly_mul, divisor)
    poly_mul      = np.array(np.mod(remainder[::-1], q), dtype=int)

    poly1_composed = poly_compose_power(poly1, 3)
    poly2_composed = poly_compose_power(poly2, 5)

    _, remainder = np.polydiv(poly1_composed[::-1], divisor)
    poly1_auto = np.array(np.mod(remainder[::-1], q), dtype=int)
    _, remainder = np.polydiv(poly2_composed[::-1], divisor)
    poly2_auto = np.array(np.mod(remainder[::-1], q), dtype=int)

    print("Polynomial addition             : ", poly_add )
    print("Polynomial multiplication       : ", poly_mul)
    print("Polynomial1 automorphism with 3 : ", poly1_auto)
    print("Polynomial2 automorphism with 5 : ", poly2_auto)
