import numpy as np
from lib.Plaintext import Plaintext

class Encoder:
    def __init__(self, params):
        self.params = params
        self.M = params.N * 2
        self.slots = params.N // 2
        self.ecdMatrices, self.dcdMatrix = GenTransformMatrices(params.N, self.M)

    # TODO: encode with an arbitrary level
    def encode(self, msg: np.ndarray) -> Plaintext:
        return NotImplemented

    def decode(self, plaintext):
        # ring element → FFT 역변환 → 복소수 벡터
        return self.params.ring.decode(plaintext)

def GenTransformMatrices(N, M):
    zeta = np.exp(2 * np.pi * 1j / M)

    U = []
    for i in range(N // 2):  # i = 0, 1, 2, 3
        tmp = [zeta ** (j * (5 ** i)) for j in range(N)]
        U.append(tmp)

    U   = np.array(U, dtype=complex)
    _U  = np.conjugate(U)
    UT  = U.T
    CRT = np.concatenate((U, _U), axis=0)

    return [_U.T, UT], CRT

def Encode(msg:np.ndarray, ecdMatrices, N: int, scale: int):
    _UT, UT = ecdMatrices
    z = np.array(msg, dtype=complex).reshape(-1,1)
    z_bar = np.conjugate(z)

    encoded = np.array(((1/N) * (_UT @ z  + UT @ z_bar)).real, dtype=np.float128)
    scaled = np.array(encoded * scale, dtype=np.float128)
    rounded = np.array(scaled, dtype=int)

    return rounded
