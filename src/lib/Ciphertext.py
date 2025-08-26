from lib.Polynomial import RingElem

class Ciphertext:
    def __init__(self, components: list["RingElem"], scale: int, level: int):
        self.components = components
        self.scale = scale
        self.level = level

    # TODO:
    def copy(self):
        return NotImplemented


