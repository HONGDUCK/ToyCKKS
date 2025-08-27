import pytest
import numpy as np
from core.parameters import CKKSParameters
from core.cryptocontext import CryptoContext


@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_ciphertext_ciphertext_addition(N):
    TESTPARAM = CKKSParameters(N, 250, 40, 3.2)
    cc = CryptoContext(TESTPARAM)
    max_level = cc.max_level
    slot_count = cc.slot_count

    secret_key = cc.keygen()
    msg1 = np.random.randint(-100, 100, size=slot_count) / 7
    msg2 = np.random.randint(-100, 100, size=slot_count) / 3
    ideal = msg1 + msg2

    for _level1 in range(max_level+1):
        for _level2 in range(max_level+1):
            ciphertext1 = cc.encrypt(msg1, secret_key, _level1)
            ciphertext2 = cc.encrypt(msg2, secret_key, _level2)

            added = cc.add(ciphertext1, ciphertext2)
            result = cc.decrypt(added, secret_key)

            assert np.allclose(ideal, result, rtol=0, atol=1e-5)
