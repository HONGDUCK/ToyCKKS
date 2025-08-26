from lib.Polynomial import RingElem

class Plaintext:
    def __init__(self, poly: "RingElem", scale: int, level: int):
        self.poly = poly        # lib.Polynomial element
        self.scale = scale      # 스케일 (예: 2**40)
        self.level = level      # 0..L (single-q면 보통 0)

    def copy(self): # TODO
        return NotImplemented
        # return Plaintext(self.poly.copy(), self.scale, self.level)

    def __repr__(self):
        return f"Plaintext(level={self.level}, scale={self.scale})"

