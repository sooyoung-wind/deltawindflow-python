from abc import ABC, abstractmethod
import math

class IDistanceCorrelationCalculator(ABC):
    @abstractmethod
    def calculate(self, *distances: float) -> float:
        pass

class DistanceCorrelationCalculator(IDistanceCorrelationCalculator):
    _root_two = math.sqrt(2)

    def __init__(self, length_scale: float):
        self.length_scale = length_scale

    def calculate(self, *distances: float) -> float:
        total = 0.0
        for distance in distances:
            total += math.exp(-self._root_two * distance / self.length_scale)
        return total / 2.0 