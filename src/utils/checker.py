import numpy as np

def _is_scalar_integer(scalar) -> bool:
    allowed_types = (int, np.integer)
    if isinstance(scalar, allowed_types):
        return True
    else:
        return False
