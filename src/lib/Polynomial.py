from __future__ import annotations
from dataclasses import dataclass
from typing import List, Iterable, Protocol, runtime_checkable, cast
import numpy as np
import random
import math
import secrets

# ---------- Utils ----------

def _to_pyint_scalar(x):
    if isinstance(x, np.ndarray):
        if x.ndim != 0:
            raise TypeError(f"Coefficient must be a scalar or 0-d array, got shape {x.shape}")
        x = x.item()
    return int(x)

# ---------- Interfaces & primitives ----------

@runtime_checkable
class ModSystem(Protocol):
    """Abstract interface for a modulus system (single q or RNS)."""
    def reduce(self, a: int) -> int: ...
    def center_reduce(self, a: int) -> int: ...
    def add(self, a: int, b: int) -> int: ...
    def sub(self, a: int, b: int) -> int: ...
    def mul(self, a: int, b: int) -> int: ...
    def negate(self, a: int) -> int: ...
    def as_int(self, a: int) -> int: ...
    def bitlen(self) -> int: ...

# TODO: q를 power-of-two 사용할 것 이므로 마스킹을 이용해서
# mod 연산 경량화
@dataclass(frozen=True)
class SingleMod(ModSystem):
    q: int
    def __post_init__(self):
        if self.q <= 1:
            raise ValueError("q must be > 1")
    def reduce(self, a: int) -> int:
        x = a % self.q
        return x if x >= 0 else x + self.q
    def center_reduce(self, a: int) -> int:
        h = self.q // 2
        return ((a + h) % self.q) - h
    def add(self, a: int, b: int) -> int: return (a + b) % self.q
    def sub(self, a: int, b: int) -> int: return (a - b) % self.q
    def mul(self, a: int, b: int) -> int: return (a * b) % self.q
    def negate(self, a: int) -> int: return (self.q - a) % self.q
    def as_int(self, a: int) -> int: return int(a)
    def bitlen(self) -> int: return self.q.bit_length()

# ---------- Cyclotomic polynomial X^N + 1 ----------

@dataclass(frozen=True)
class Cyclotomic2N:
    N: int  # power-of-two typical
    def __post_init__(self):
        if self.N <= 0:
            raise ValueError("N must be positive")
    @property
    def degree(self) -> int: return self.N

# ---------- Polynomial representations ----------

class Poly:
    """Dense polynomial over Z_q with modulus X^N + 1 (coeffs length N)."""
    __slots__ = ("coeffs", "mod", "N")
    def __init__(self, coeffs: Iterable[int], mod: ModSystem, N: int):
        coeffs = list(coeffs)
        if len(coeffs) != N:
            raise ValueError(f"need {N} coeffs")
        self.mod = mod
        self.N = N
        self.coeffs = np.array([mod.reduce(_to_pyint_scalar(c)) for c in coeffs], dtype=object)

    @classmethod
    def zero(cls, mod: ModSystem, N: int) -> "Poly":
        return cls([0]*N, mod, N)

    @classmethod
    def from_int(cls, k: int, mod: ModSystem, N: int) -> "Poly":
        v = [0]*N
        v[0] = mod.reduce(k)
        return cls(v, mod, N)

    def copy(self) -> "Poly": return Poly(self.coeffs.tolist(), self.mod, self.N)

    # ring ops
    def __add__(self, other: "Poly") -> "Poly":
        self._check(other)
        c = (self.coeffs + other.coeffs) % self._q_like()
        return Poly(c, self.mod, self.N)

    def __sub__(self, other: "Poly") -> "Poly":
        self._check(other)
        c = (self.coeffs - other.coeffs) % self._q_like()
        return Poly(c, self.mod, self.N)

    def __neg__(self) -> "Poly":
        q = self._q_like()
        return Poly((-self.coeffs) % q, self.mod, self.N)

    def scalarmul(self, k: int) -> "Poly":
        q = self._q_like()
        return Poly((self.coeffs * (k % int(q))) % q, self.mod, self.N)

    def mul(self, other: "Poly", method: str = "schoolbook") -> "Poly":
        self._check(other)
        if method == "schoolbook":
            return self._mul_schoolbook(other)
        elif method == "ntt":
            raise NotImplementedError("attach NTTParams and implement")
        else:
            raise ValueError("unknown method")

    # X^N + 1 reduction: cyclic negacyclic convolution
    def _mul_schoolbook(self, other: "Poly") -> "Poly":
        q = self._q_like()
        N = self.N
        a = self.coeffs
        b = other.coeffs
        # naive O(N^2) negacyclic convolution
        acc = np.zeros(N, dtype=object)
        for i in range(N):
            ai = a[i]
            if ai == 0: continue
            for j in range(N):
                k = i + j
                if k < N:
                    acc[k] = (acc[k] + ai * b[j]) % q
                else:
                    acc[k - N] = (acc[k - N] - ai * b[j]) % q  # negate due to X^N = -1
        return Poly(acc, self.mod, N)

    # TODO: permutation map 으로 만들어두어 연산 경량화
    def automorphism(self, k: int) -> "Poly":
        N = self.N
        M = 2 * N
        k %= M
        # Note: N 이 power-of-two 일 경우에는 홀수 여부만 판단하면 됨.
        if k % 2 == 0 or math.gcd(k, M) != 1:
            raise ValueError("k must be odd and coprime to 2N")

        q = self._q_like()
        a = self.coeffs
        res = np.zeros(N, dtype=object)

        for i in range(N):
            j = (i * k) % M
            if j < N:
                # X^i -> X^(ik), same sign
                res[j] = a[i]  # already reduced
            else:
                # X^i -> -X^(ik - N) because X^N = -1
                res[j - N] = (-a[i]) % q

        return Poly(res, self.mod, N)

    def tolist(self) -> List[int]: return [int(x) for x in self.coeffs]

    def _q_like(self):
        return int(cast(SingleMod, self.mod).q)

    def _center_reduce(self):
        mod = self.mod
        coeffs = self.coeffs
        return np.array([mod.center_reduce(
            _to_pyint_scalar(c)) for c in coeffs], dtype=object)

    def _check(self, other: "Poly"):
        if self.N != other.N or type(self.mod) != type(other.mod):
            raise TypeError("incompatible polynomials")

# ---------- Ring & elements ----------

@dataclass
class CyclotomicRing:
    N: int
    modsys: ModSystem
    poly: Cyclotomic2N

    @classmethod
    def create(cls, N: int, modsys: ModSystem) -> "CyclotomicRing":
        return cls(N=N, modsys=modsys, poly=Cyclotomic2N(N))

    def from_coeffs(self, coeffs: Iterable[int]) -> "RingElem":
        return RingElem(self, Poly(coeffs, self.modsys, self.N))
    def zero(self) -> "RingElem": return RingElem(self, Poly.zero(self.modsys, self.N))
    def one(self) -> "RingElem": return RingElem(self, Poly.from_int(1, self.modsys, self.N))
    def random_uniform(self) -> "RingElem":
        if isinstance(self.modsys, SingleMod):
            q = self.modsys.q
            coeffs = [secrets.randbelow(q) for _ in range(self.N)]
            return RingElem(self, Poly(coeffs, self.modsys, self.N))
        else: # For RNS variant
            raise RuntimeError("Not implemented yet")
    def sample_ternary(self) -> "RingElem":
        if isinstance(self.modsys, SingleMod):
            coeffs = [secrets.randbelow(3) - 1 for _ in range(self.N)]
            return RingElem(self, Poly(coeffs, self.modsys, self.N))
        else: # For RNS variant
            raise RuntimeError("Not implemented yet")
    def sample_Gaussian(self, sigma=3.2) -> "RingElem":
            coeffs = [round(random.gauss(0, sigma)) for _ in range(self.N)]
            return RingElem(self, Poly(coeffs, self.modsys, self.N))

@dataclass
class RingElem:
    ring: CyclotomicRing
    poly: Poly

    def __post_init__(self):
        if self.poly.N != self.ring.N:
            raise ValueError("degree mismatch")

    # Ring operations
    def __add__(self, other: "RingElem") -> "RingElem":
        self._check(other); return RingElem(self.ring, self.poly + other.poly)
    def __sub__(self, other: "RingElem") -> "RingElem":
        self._check(other); return RingElem(self.ring, self.poly - other.poly)
    def __neg__(self) -> "RingElem":
        return RingElem(self.ring, -self.poly)
    def scalarmul(self, k: int) -> "RingElem":
        return RingElem(self.ring, self.poly.scalarmul(k))
    def __mul__(self, other: "RingElem") -> "RingElem":
        self._check(other); return RingElem(self.ring, self.poly.mul(other.poly, method="schoolbook"))
    def Auto(self, k: int) -> "RingElem":
        return RingElem(self.ring, self.poly.automorphism(k))

    def tolist(self) -> List[int]: return self.poly.tolist()

    def _check(self, other: "RingElem"):
        if self.ring is not other.ring:
            # Strict: require same ring instance; relax if needed by checking N & modsys equality.
            raise TypeError("elements from different rings")


''' Notes
class CyclotomicRing:
    ...
    def automorphism_map(self, k: int):
        """Precompute target indices and signs (+1/-1) for X -> X^k."""
        N = self.N
        M = 2 * N
        k %= M
        if k % 2 == 0 or math.gcd(k, M) != 1:
            raise ValueError("k must be odd and coprime to 2N")
        perm = [0] * N     # target index in [0, N)
        sign = [1] * N     # +1 or -1
        for i in range(N):
            j = (i * k) % M
            if j < N:
                perm[i] = j
                sign[i] = 1
            else:
                perm[i] = j - N
                sign[i] = -1
        return np.array(perm, dtype=int), np.array(sign, dtype=int)

class Poly:
    ...
    def automorphism_with_map(self, perm: np.ndarray, sign: np.ndarray) -> "Poly":
        """Apply a precomputed automorphism map (perm, sign)."""
        if len(perm) != self.N or len(sign) != self.N:
            raise ValueError("bad map shape")
        q = self._q_like()
        res = np.zeros(self.N, dtype=object)
        for i in range(self.N):
            j = int(perm[i])
            if sign[i] == 1:
                res[j] = self.coeffs[i]
            else:
                res[j] = (-self.coeffs[i]) % q
        return Poly(res, self.mod, self.N)
'''
