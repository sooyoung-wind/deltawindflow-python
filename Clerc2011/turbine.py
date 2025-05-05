from dataclasses import dataclass

@dataclass(frozen=True)
class Turbine:
    x: float
    y: float

    def __eq__(self, other):
        if not isinstance(other, Turbine):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y)) 