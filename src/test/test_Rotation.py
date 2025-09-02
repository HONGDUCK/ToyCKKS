import pytest
import numpy as np
from lib.Plaintext import Plaintext
from core.parameters import CKKSParameters
from core.cryptocontext import CryptoContext

@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_plaintext_rotation(N):
    TESTPARAM = CKKSParameters(N, 250, 40, 300, 3.2)
    cc = CryptoContext(TESTPARAM)
    max_level = cc.max_level
    slot_count = cc.slot_count

    for _level in range(max_level+1):
        shift = np.random.randint(0, slot_count) 
        msg = np.random.randint(-10, 10, size=slot_count) / 7
        ideal = np.roll(msg, -shift)

        plaintext = cc.encode(msg, _level)
        automorphismed = plaintext.ringelem.Auto(5 ** shift)
        rotated = Plaintext(automorphismed, plaintext.scale, plaintext.level)
        decoded = cc.decode(rotated)

        assert np.allclose(ideal, decoded, rtol=0, atol=1e-5)

@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_ciphertext_rotation(N):
    TESTPARAM = CKKSParameters(N, 250, 40, 300, 3.2)
    cc = CryptoContext(TESTPARAM)
    max_level = cc.max_level
    slot_count = cc.slot_count

    secret_key = cc.keygen()

    for _level in range(max_level + 1):
        shift = np.random.randint(0, slot_count) 
        rotation_key = cc.rotation_keygen(shift, secret_key)
        msg = np.random.randint(-10, 10, size=slot_count) / 7
        ideal = np.roll(msg, -shift)

        ciphertext = cc.encrypt(msg, secret_key, _level)
        rotated = cc.rotate(ciphertext, rotation_key)
        result = cc.decrypt(rotated, secret_key)

        assert np.allclose(ideal, result)
