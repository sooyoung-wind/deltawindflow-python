from abc import ABC, abstractmethod
import math
from .mast_to_turbine_variation_calculator import IMastToTurbineVariationCalculator
from .speedup_variation_calculator import ISpeedupVariationCalculator

class ICoefficientOfVariationCalculator(ABC):
    @abstractmethod
    def calculate(self, mast_turbine_separation: float, speedup: float) -> float:
        pass

class CoefficientOfVariationCalculator(ICoefficientOfVariationCalculator):
    def __init__(self, mast_to_turbine_variation_calculator: IMastToTurbineVariationCalculator, speedup_variation_calculator: ISpeedupVariationCalculator):
        self.mast_to_turbine_variation_calculator = mast_to_turbine_variation_calculator
        self.speedup_variation_calculator = speedup_variation_calculator

    def calculate(self, mast_turbine_separation: float, speedup: float) -> float:
        return math.sqrt(
            self.mast_to_turbine_variation_calculator.calculate(mast_turbine_separation) ** 2 +
            self.speedup_variation_calculator.calculate(speedup) ** 2
        ) 