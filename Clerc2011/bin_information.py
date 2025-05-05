from dataclasses import dataclass
from .turbine import Turbine
from .mast import Mast

@dataclass(frozen=True)
class BinInformation:
    turbine: Turbine
    mast: Mast
    direction: float
    speedup: float
    sensitivity_factor: float
    bin_energy: float

    def __eq__(self, other):
        if not isinstance(other, BinInformation):
            return False
        return (
            self.turbine == other.turbine and
            self.mast == other.mast and
            self.direction == other.direction and
            self.speedup == other.speedup and
            self.sensitivity_factor == other.sensitivity_factor and
            self.bin_energy == other.bin_energy
        )

    def __hash__(self):
        return hash((self.turbine, self.mast, self.direction, self.speedup, self.sensitivity_factor, self.bin_energy)) 