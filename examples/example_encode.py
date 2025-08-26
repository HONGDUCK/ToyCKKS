import numpy as np

M = 16  # 2N
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

def pad_coeffs(poly, N):
    """Pads coeffs with zeros to length n if necessary."""
    if len(poly) < N:
        return np.pad(poly, (0, N - len(poly)), 'constant')
    return poly

def Nega_conv(poly1, poly2):
    N = max(len(poly1), len(poly2))
    result = []
    poly1 = pad_coeffs(poly1, N)
    poly2 = pad_coeffs(poly2, N)
    for k in range(N):
        v = 0
        for i in range(k+1):
            v += poly1[i] * poly2[k-i]
        for i in range(k+1, N):
            v -= poly1[i] * poly2[(k + N - i)]

        result.append(v)
    return result

def Encode(msg):
    z = np.array(msg, dtype=complex).reshape(-1,1)
    z_bar = np.conjugate(z)

    return ((1/N) * (U_bar.T @ z  + UT @ z_bar)).real

def Decode(ptxt):
    return (CRT @ ptxt)[:N // 2].real

if __name__ == '__main__':
    msg1 = [4, 5, 3, 4]
    msg2 = [10, 20, 30, 40]
    ptxt1 = Encode(msg1)
    ptxt2 = Encode(msg2)

    ptxt3 = Nega_conv(ptxt1, ptxt2)

    msg3 = Decode(ptxt3)

    print(msg3.T)
