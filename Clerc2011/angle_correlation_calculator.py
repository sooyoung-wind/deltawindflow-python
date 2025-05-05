from abc import ABC, abstractmethod

class IAngleCorrelationCalculator(ABC):
    @abstractmethod
    def calculate(self, delta_theta: float) -> float:
        pass

class AngleCorrelationCalculator(IAngleCorrelationCalculator):
    def calculate(self, delta_theta: float) -> float:
        return max(1 - abs(delta_theta) / 90.0, 0) 