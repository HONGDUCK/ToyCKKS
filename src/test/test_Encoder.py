import numpy as np
import pytest
from core.encoder import Encoder
from core.parameters import CKKSParameters

def TransformationMatricesGen(N):
    U = []
    for i in range(N // 2):
        pow5_mod2N = pow(5, i, 2*N)
        angles = (np.arange(N) * pow5_mod2N) % (2*N)
        theta = np.pi * angles / N
        tmp = np.exp(1j * theta)
        U.append(tmp)

    U   = np.array(U, dtype=complex)
    _U  = np.conjugate(U)
    UT  = U.T
    _UT = _U.T
    CRT = np.concatenate((U, _U), axis=0)

    return [_UT, UT], CRT

def unit_encode(msg, N, ecdM):
    _UT , UT = ecdM
    z = np.array(msg, dtype=complex).reshape(-1,1)
    z_bar = np.conjugate(z)

    return ((1/N) * (_UT @ z  + UT @ z_bar)).real

def unit_decode(plaintext, N, dcdM):
    return (dcdM @ plaintext)[:N // 2].T.real

@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_encode(N):
    for _ in range(10):
        slot_count = N//2
        msg = np.array(np.random.rand(slot_count))

        TESTPARAM = CKKSParameters(N, 250, 40, 300, 3.2)
        encoder = Encoder(TESTPARAM)

        plaintext = encoder.encode(msg)
        cleartext = encoder.decode(plaintext)

        assert np.allclose(cleartext, msg, rtol=0, atol=1e-5)
