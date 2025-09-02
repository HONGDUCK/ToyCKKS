# Beginner guide of fully homomorphic encryption and it's toy implementation : CKKS (Korean)

---

CKKS (Cheon, Kim, Kim, Song) 은 동형암호 최초의 실수 연산을 지원하는 스킴입니다.
PPML (Privacy-preserving machine learning) 등 다양한 분야에서 활용되고 있으며 현재까지도 많은 연구가 진행되고 있는 유용한 동형암호 시스템입니다.

여기에서는 처음 CKKS 를 접하는 사람들을 위한 가이드를 제공하는 것을 목표하고 있습니다.
다음과 같은 논문들을 익히는 것을 목표로 진행합니다.

1. <a href="https://eprint.iacr.org/2016/421"> Homomorphic Encryption for Arithmetic of Approximate Numbers </a>, Cheon et al.
2. <a href="https://eprint.iacr.org/2018/153"> Bootstrapping for Approximate Homomorphic Encryption </a>, Cheon et al.

---
## How to run

```
pip install -e .
python examples/example_...
```

---

## Leveled CKKS (Done)
> 구현된 기능들   
> [Encoding/Decoding, Encryption/Decryption, Addition, Multiplication, Rotation, Relinearization, KeySwitching]

1. Ring $\mathcal{R}_Q$ 에서의 연산의 종류들과 정의들 
2. $\mathcal{R}_Q$ 에서 정의되는 곱셈과 CKKS 에서 제공하는 element-wise 곱셈과의 관계 (Encoding/Decoding) 
3. CKKS 곱셈에서 노이즈를 조절하는 방법 (Multiplication, Rescale, Relinearization) 
4. Automorphism (1 에서 학습) 과 CKKS 에서 제공하는 shift 연산과의 관계 (Rotation, Key switching) 
5. Lectures/Docs 작업 🏃

---

## FHE CKKS : Bootstrapping (Working)

1. Multiplication 과 rotation 을 이용한 vector-matrix multiplication.
2. Multiplication 을 이용한 polynomial evaluation: power-basis
3. Multiplication 을 이용한 chebyshev evaluation: chebyshev-basis
4. Ciphertext modulus 와 hamming weight 그리고 modulus raise
5. Matrix multiplication 을 이용한 homomorphic encoding : coeff-to-slot
6. Matrix multiplication 을 이용한 homomorphic decoding : slot-to-coeff
7. Homomorphic modulus 연산 : EvalMod
8. Bootstrapping

---

## Optimizations (고민)
1. NTT (Cooley Tukey algorithm)
2. RNS-CKKS (<a href="https://eprint.iacr.org/2018/931"> A Full RNS Variant of Approximate Homomorphic Encryption </a>, Cheon et al.)

> 최근에 일이 바빠져서 언제 마무리 지을 수 있을지는 모르겠지만, 시간 날 때 마다 틈틈히 해보겠습니다.

