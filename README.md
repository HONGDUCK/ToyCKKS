# Beginner guide of fully homomorphic encryption and it's toy implementation : CKKS (Korean)

---

CKKS (Cheon, Kim, Kim, Song) 은 동형암호 최초의 실수 연산을 지원하는 스킴입니다.
PPML (Privacy-preserving machine learning) 등 다양한 분야에서 활용되고 있으며 현재까지도 많은 연구가 진행되고 있는 유용한 동형암호 시스템입니다.

여기에서는 처음 CKKS 를 접하는 사람들을 위한 가이드를 제공하는 것을 목표하고 있습니다.
다음과 같은 논문들을 익히는 것을 목표로 진행합니다.

1. <a href="https://eprint.iacr.org/2016/421"> Homomorphic Encryption for Arithmetic of Approximate Numbers </a>, Cheon et al.
2. <a href="https://eprint.iacr.org/2018/931"> A Full RNS Variant of Approximate Homomorphic Encryption </a>, Cheon et al.
3. <a href="https://eprint.iacr.org/2018/153"> Bootstrapping for Approximate Homomorphic Encryption </a>, Cheon et al.

---

배우는 것들을 크게 다음과 같이 구분화 합니다.

1. Ring $\mathcal{R}_Q$ 에서의 연산의 종류들과 정의들

2. Ring $\mathcal{R}_{Q}$ 을 RNS-variant 으로 확장.

3. $\mathcal{R}_Q$ 에서 정의되는 곱셈과 CKKS 에서 제공하는 element-wise 곱셈과의 관계 (Encoding/Decoding)

4. CKKS 에서 노이즈를 조절하는 방법 (Rescale, Relinearization, Key switching)

5. Automorphism (1 에서 학습) 과 CKKS 에서 제공하는 shift 연산과의 관계 (Rotation)

6. CKKS 곱셈을 이용한 다항식 연산과 근사 다항식을 통한 임의의 함수 연산 $f$의 수행

7. (6) 을 Chebyshev 근사로의 확장과 Chebyshev 근사의 유용성

8. Bootstrapping

---

> 최근의 일이 바빠져서 언제 마무리 지을 수 있을지는 모르겠지만, 시간 날 때 마다 틈틈히 해보겠습니다.

