from abc import ABC, abstractmethod

class ISpeedupVariationCalculator(ABC):
    @abstractmethod
    def calculate(self, speedup: float) -> float:
        pass

class SpeedupVariationCalculator(ISpeedupVariationCalculator):
    def __init__(self, a: float):
        self.a = a

    def calculate(self, speedup: float) -> float:
        return 2 * self.a * abs(speedup - 1) / (speedup + 1)

class OffshoreSpeedupVariationCalculator(ISpeedupVariationCalculator):
    def calculate(self, speedup: float) -> float:
        return 0.0 