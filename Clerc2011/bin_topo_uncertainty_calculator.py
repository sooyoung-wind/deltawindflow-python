from abc import ABC, abstractmethod
import math
from .bin_information import BinInformation
from .coefficient_of_variation_calculator import ICoefficientOfVariationCalculator
from .correlation_calculator import ICorrelationCalculator

class IBinTopoUncertaintyCalculator(ABC):
    @abstractmethod
    def calculate_variance(self, bin: BinInformation) -> float:
        pass

    @abstractmethod
    def calculate(self, bin1: BinInformation, bin2: BinInformation, variance1: float, variance2: float) -> float:
        pass

class BinTopoUncertaintyCalculator(IBinTopoUncertaintyCalculator):
    def __init__(self, coefficient_of_variation_calculator: ICoefficientOfVariationCalculator, correlation_calculator: ICorrelationCalculator):
        self.coefficient_of_variation_calculator = coefficient_of_variation_calculator
        self.correlation_calculator = correlation_calculator

    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def _get_angle_difference(self, dir1, dir2):
        diff = dir1 - dir2
        if diff > 180:
            return diff - 360
        elif diff < -180:
            return diff + 360
        else:
            return diff

    def calculate_variance(self, bin: BinInformation) -> float:
        return self.coefficient_of_variation_calculator.calculate(
            self._distance(bin.turbine.x, bin.turbine.y, bin.mast.x, bin.mast.y),
            bin.speedup
        )

    def _calculate_coefficient(self, bin1: BinInformation, bin2: BinInformation) -> float:
        return self.correlation_calculator.calculate(
            self._get_angle_difference(bin1.direction, bin2.direction),
            self._distance(bin1.mast.x, bin1.mast.y, bin2.mast.x, bin2.mast.y),
            self._distance(bin1.turbine.x, bin1.turbine.y, bin2.turbine.x, bin2.turbine.y)
        )

    def calculate(self, bin1: BinInformation, bin2: BinInformation, variance1: float, variance2: float) -> float:
        return (
            self._calculate_coefficient(bin1, bin2)
            * variance1 * variance2
            * bin1.sensitivity_factor * bin2.sensitivity_factor
        )

    def calculate_default(self, bin1: BinInformation, bin2: BinInformation) -> float:
        v1 = self.calculate_variance(bin1)
        v2 = self.calculate_variance(bin2)
        return self.calculate(bin1, bin2, v1, v2) 