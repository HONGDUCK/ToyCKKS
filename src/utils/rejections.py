import numpy as np
from lib.Plaintext import Plaintext
from lib.Ciphertext import Ciphertext

# 암호문의 poly 가 튜플인지 체크
def _check_ciphertext_components(ct: "Ciphertext"):
    if len(ct.components) != 2:
        raise RuntimeError("Ciphertext components should be two.")

# 암호문의 레벨이 타겟보다 작은지 체크
def _is_small_level_ct(ct: "Ciphertext", target_level: int):
    if ct.level < target_level:
        raise RuntimeError("Target level should be smaller then current level : Ciphertext")

# 평문의 레벨이 타겟보다 작은지 체크
def _is_small_level_pt(pt: "Plaintext", target_level: int):
    if pt.level < target_level:
        raise RuntimeError("Target level should be smaller then current level : Plaintext")

# 메세지의 수가 slot의 수와 동일한지 체크
def _check_msg_length(msg: np.ndarray, slot_count: int):
    if len(msg) != slot_count:
        raise RuntimeError("Invalied message length")

# 스칼라가 정수 혹은 실수인지 확인하는 체커
def _valid_scalar(x):
    allowed_types = (int, float, np.integer, np.floating)
    if not isinstance(x, allowed_types):
        raise ValueError(f"Invalid type {type(x)}: only {allowed_types} allowed")
    return x

def _valid_array_dtype(arr: np.ndarray):
    if np.issubdtype(arr.dtype, np.integer):
        pass
    elif np.issubdtype(arr.dtype, np.floating):
        pass
    else:
        raise ValueError(f"Unsupported dtype {arr.dtype}, only int or float arrays are allowed")

