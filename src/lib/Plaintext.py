from lib.Polynomial import RingElem

class Plaintext:
    def __init__(self, ringelem: "RingElem", scale: int, level: int):
        self.ringelem = ringelem
        self.scale = scale
        self.level = level

    # TODO: 좀 더 다듬기
    def copy(self): # TODO
        return NotImplemented
        # return Plaintext(self.poly.copy(), self.scale, self.level)

    def __repr__(self):
        formatted = ""
        for idx, x in enumerate(self.ringelem.tolist()):
            formatted += f"{float(x):.3e} "
            if idx % 4 == 3:
                formatted += "\n"
        return (f"Plaintext(level={self.level}, scale={self.scale}), coeffs:\n"
                +f"{formatted}")

