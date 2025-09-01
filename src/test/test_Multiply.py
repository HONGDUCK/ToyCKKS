import pytest
import numpy as np
from core.parameters import CKKSParameters
from core.cryptocontext import CryptoContext

@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_ciphertext_int_multiplication(N):
    TESTPARAM = CKKSParameters(N, 250, 40, 300, 3.2)
    cc = CryptoContext(TESTPARAM)
    max_level = cc.max_level
    slot_count = cc.slot_count

    secret_key = cc.keygen()

    for _level in range(max_level+1):
        msg = np.random.randint(-10, 10, size=slot_count) / 7
        scalar = np.random.randint(-10, 10)
        ideal = msg * scalar

        ciphertext = cc.encrypt(msg, secret_key, _level)
        added = cc.mul_scalar(ciphertext, scalar)
        result = cc.decrypt(added, secret_key)

        assert np.allclose(ideal, result, rtol=0, atol=1e-5)

@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_ciphertext_double_multiplication(N):
    TESTPARAM = CKKSParameters(N, 250, 40, 300, 3.2)
    cc = CryptoContext(TESTPARAM)
    max_level = cc.max_level
    slot_count = cc.slot_count

    secret_key = cc.keygen()

    for _level in range(1, max_level+1):
        msg = np.random.randint(-10, 10, size=slot_count) / 7
        scalar = np.random.randint(-10, 10) / 3
        ideal = msg * scalar

        ciphertext = cc.encrypt(msg, secret_key, _level)
        added = cc.mul_scalar(ciphertext, scalar)
        result = cc.decrypt(added, secret_key)

        assert np.allclose(ideal, result, rtol=0, atol=1e-5)

@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_ciphertext_messages_multiplication(N):
    TESTPARAM = CKKSParameters(N, 250, 40, 300, 3.2)
    cc = CryptoContext(TESTPARAM)
    max_level = cc.max_level
    slot_count = cc.slot_count

    secret_key = cc.keygen()

    for _level in range(1, max_level+1):
        msg1 = np.random.randint(-10, 10, size=slot_count) / 7
        msg2 = np.random.randint(-10, 10, size=slot_count) / 3
        ideal = msg1 * msg2

        ciphertext = cc.encrypt(msg1, secret_key, _level)
        added = cc.mul_messages(ciphertext, msg2)
        result = cc.decrypt(added, secret_key)

        assert np.allclose(ideal, result, rtol=0, atol=1e-5)

@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_ciphertext_ciphertext_multiplication(N):
    TESTPARAM = CKKSParameters(N, 250, 40, 300, 3.2)
    cc = CryptoContext(TESTPARAM)
    max_level = cc.max_level
    slot_count = cc.slot_count

    secret_key = cc.keygen()
    relinearization_key = cc.relinearization_keygen(secret_key)

    for _level1 in range(1, max_level+1):
        for _level2 in range(1, max_level+1):
            msg1 = np.random.randint(-10, 10, size=slot_count) / 7
            msg2 = np.random.randint(-10, 10, size=slot_count) / 3
            ideal = msg1 * msg2

            ciphertext1 = cc.encrypt(msg1, secret_key, _level1)
            ciphertext2 = cc.encrypt(msg2, secret_key, _level2)
            added = cc.mul(ciphertext1, ciphertext2, relinearization_key)
            result = cc.decrypt(added, secret_key)

            assert np.allclose(ideal, result, rtol=0, atol=1e-5)
