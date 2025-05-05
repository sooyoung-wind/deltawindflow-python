from dataclasses import dataclass
from .mast import Mast

@dataclass(frozen=True)
class MastWeighting:
    mast: Mast
    results_weighting: float 