from abc import ABC, abstractmethod
from .angle_correlation_calculator import IAngleCorrelationCalculator
from .distance_correlation_calculator import IDistanceCorrelationCalculator

class ICorrelationCalculator(ABC):
    @abstractmethod
    def calculate(self, delta_theta: float, mast_mast_distance: float, turbine_turbine_distance: float) -> float:
        pass

class CorrelationCalculator(ICorrelationCalculator):
    def __init__(self, angle_correlation_calculator: IAngleCorrelationCalculator, distance_correlation_calculator: IDistanceCorrelationCalculator):
        self.angle_correlation_calculator = angle_correlation_calculator
        self.distance_correlation_calculator = distance_correlation_calculator

    def calculate(self, delta_theta: float, mast_mast_distance: float, turbine_turbine_distance: float) -> float:
        return (
            self.angle_correlation_calculator.calculate(delta_theta)
            * self.distance_correlation_calculator.calculate(mast_mast_distance, turbine_turbine_distance)
        ) 