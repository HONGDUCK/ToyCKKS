import pytest
import numpy as np
from core.key_generator import KeyGenerator
from core.encoder import Encoder
from core.encryptor import Encryptor
from core.parameters import CKKSParameters


@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_encrypt(N):
    for _ in range(10):
        slot_count = N//2
        msg = np.array(np.random.rand(slot_count))

        TESTPARAM = CKKSParameters(N, 250, 40, 3.2)
        encoder = Encoder(TESTPARAM)
        encryptor = Encryptor(TESTPARAM)
        keyGenerator = KeyGenerator(TESTPARAM)

        secret_key = keyGenerator.gen_secret_key()

        plaintext = encoder.encode(msg)
        ciphertext = encryptor.encrypt(plaintext, secret_key)
        decrypted = encryptor.decrypt(ciphertext, secret_key)
        cleartext = encoder.decode(decrypted)

        assert np.allclose(cleartext, msg, rtol=0, atol=1e-5)
