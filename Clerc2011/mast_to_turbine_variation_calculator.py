from abc import ABC, abstractmethod
import math

class IMastToTurbineVariationCalculator(ABC):
    @abstractmethod
    def calculate(self, distance_mast_turbine: float) -> float:
        pass

class MastToTurbineVariationCalculator(IMastToTurbineVariationCalculator):
    def __init__(self, lamda: float, length_scale: float):
        self.lamda = lamda
        self.length_scale = length_scale

    def calculate(self, distance_mast_turbine: float) -> float:
        return self.lamda * (1 - math.exp(-distance_mast_turbine / self.length_scale)) 