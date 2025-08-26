import numpy as np
from core.parameters import TOY
from core.encoder import Encoder

# N 이 크면 Overflow 발생함.
M = 32  # 2N
N = M // 2
zeta = np.exp(2 * np.pi * 1j / M)

U = []
for i in range(N // 2):  # i = 0, 1, 2, 3
    tmp = [zeta ** (j * (5 ** i)) for j in range(N)]
    U.append(tmp)

U = np.array(U, dtype=complex)  # (4, 8)
U_bar = np.conjugate(U)         # (4, 8)
UT = U.T                        # (8, 4)
UT_bar = np.conjugate(UT)       # (8, 4)
CRT = np.concatenate((U, U_bar), axis=0)

def Encode(msg):
    z = np.array(msg, dtype=complex).reshape(-1,1)
    z_bar = np.conjugate(z)

    return ((1/N) * (U_bar.T @ z  + UT @ z_bar)).real

def Decode(ptxt):
    return (CRT @ ptxt)[:N // 2].T.real

if __name__ == '__main__':

    msg = np.array([4, 5, 3, 4, 4, 5, 3, 4], dtype=np.complex128) / 3

    print("====== Ours ======")
    encoder = Encoder(TOY)

    plaintext = encoder.encode(msg)
    cleartext = encoder.decode(plaintext)

    print(plaintext)
    print(msg.real)
    print(cleartext)

    print("====== Ideal ======")

    plaintext_ideal = Encode(msg)
    cleartext_ideal = Decode(plaintext_ideal)

    print(plaintext_ideal.T)
    print(msg.real)
    print(cleartext_ideal)
