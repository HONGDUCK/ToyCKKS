import numpy as np
from lib.Plaintext import Plaintext

class Encoder:
    def __init__(self, params):
        self.params = params
        self.slots = params.N // 2
        self.ecdMatrices, self.dcdMatrix = GenTransformMatrices(params.N)

    # TODO: encode with an arbitrary level
    def encode(self, msg: np.ndarray) -> "Plaintext":
        cycloRing = self.params.ring
        complex_msg = np.array([m for m in msg], dtype=np.complex128)
        rounded = Encode(complex_msg, self.ecdMatrices, self.params.N, self.params.scale)
        encoded = cycloRing.from_coeffs(rounded)
        return Plaintext(encoded, self.params.scale, self.params.max_level)

    def decode(self, plaintext: "Plaintext") -> np.ndarray:
        current_level = plaintext.level
        log_modulus = self.params.log_modulus_table[current_level]
        decoded = Decode(plaintext, self.dcdMatrix, self.params.N, self.params.scale, log_modulus)
        return decoded

def GenTransformMatrices(N):
    U = []
    for i in range(N // 2):
        pow5_mod2N = pow(5, i, 2*N)        # 이제 모듈로는 2N (2N차 원시근이니까)
        angles = (np.arange(N) * pow5_mod2N) % (2*N)
        theta = np.pi * angles / N         # 2π/(2N) = π/N
        tmp = np.exp(1j * theta)
        U.append(tmp)

    U   = np.array(U, dtype=complex)
    _U  = np.conjugate(U)
    UT  = U.T
    _UT = _U.T
    CRT = np.concatenate((U, _U), axis=0)

    return [_UT, UT], CRT

def Encode(msg:np.ndarray, ecdMatrices, N: int, scale: int):
    _UT, UT = ecdMatrices
    z = np.array(msg, dtype=complex).reshape(-1,1)
    z_bar = np.conjugate(z)

    encoded = np.array(((1/N) * (_UT @ z  + UT @ z_bar)).real, dtype=np.float64)
    scaled = np.array(encoded * scale, dtype=np.float64)
    rounded = np.array(np.round(scaled), dtype=int)

    return rounded.flatten()

def Decode(plaintext: "Plaintext", dcdMatrix, N:int, scale: int, log_modulus: int):
    modulus = 1 << int(log_modulus)
    coeffs = np.array(plaintext.ringelem.tolist(), dtype=object)
    reduced = np.array(np.mod(coeffs, modulus), dtype=object) # hardcoded
    centered = np.array(np.where(reduced > modulus // 2, reduced - modulus, reduced), dtype=object)
    scaled = np.array(centered / scale, dtype=np.float64)
    transformed = np.array((dcdMatrix @ scaled)[:N//2].T.real, dtype=np.float64)
    return transformed
