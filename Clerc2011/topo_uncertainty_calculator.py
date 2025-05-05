from typing import Dict, List, Iterable
from .turbine import Turbine
from .mast_weighting import MastWeighting
from .bin_information import BinInformation
from .bin_topo_uncertainty_calculator import BinTopoUncertaintyCalculator
from .coefficient_of_variation_calculator import CoefficientOfVariationCalculator
from .mast_to_turbine_variation_calculator import MastToTurbineVariationCalculator
from .speedup_variation_calculator import SpeedupVariationCalculator, OffshoreSpeedupVariationCalculator
from .correlation_calculator import CorrelationCalculator
from .angle_correlation_calculator import AngleCorrelationCalculator
from .distance_correlation_calculator import DistanceCorrelationCalculator
import threading
import math

class TopoUncertaintyCalculator:
    def __init__(self, lamda: float, length_scale: float, a: float, mast_weightings: Dict[Turbine, Iterable[MastWeighting]], offshore: bool):
        speedup_var_calc = OffshoreSpeedupVariationCalculator() if offshore else SpeedupVariationCalculator(a)
        self._bin_topo_uncertainty_calculator = BinTopoUncertaintyCalculator(
            CoefficientOfVariationCalculator(
                MastToTurbineVariationCalculator(lamda, length_scale),
                speedup_var_calc
            ),
            CorrelationCalculator(
                AngleCorrelationCalculator(),
                DistanceCorrelationCalculator(length_scale)
            )
        )
        self._mast_weightings = mast_weightings
        self._values: List[BinInformation] = []
        self._lock = threading.Lock()

    def _get_mast_weight(self, turbine: Turbine, mast) -> float:
        return self._get_mast_weight_from_list(self._mast_weightings[turbine], mast)

    def _get_mast_weight_from_list(self, mast_weightings: Iterable[MastWeighting], mast) -> float:
        filtered = [w for w in mast_weightings if w.mast == mast]
        if len(filtered) != 1:
            return 0.0
        return filtered[0].results_weighting

    def _calculate_uncertainty(self, values: Iterable[BinInformation]) -> float:
        bins = list(values)
        count = len(bins)
        mast_weights = [0.0] * count
        variance = [0.0] * count
        total = 0.0
        for i in range(count):
            if bins[i].bin_energy > 0 and bins[i].sensitivity_factor > 0:
                mast_weights[i] = self._get_mast_weight(bins[i].turbine, bins[i].mast)
                if mast_weights[i] > 0:
                    variance[i] = self._bin_topo_uncertainty_calculator.calculate_variance(bins[i])
                    if variance[i] > 0:
                        for j in range(i+1):
                            if bins[j].bin_energy > 0 and mast_weights[j] > 0 and bins[j].sensitivity_factor > 0 and variance[j] > 0:
                                single_result = self._bin_topo_uncertainty_calculator.calculate(
                                    bins[i], bins[j], variance[i], variance[j]
                                ) * bins[i].bin_energy * bins[j].bin_energy * mast_weights[i] * mast_weights[j]
                                if i != j:
                                    single_result *= 2
                                total += single_result
        return math.sqrt(total)

    @property
    def energy(self) -> float:
        return sum(bin1.bin_energy * self._get_mast_weight(bin1.turbine, bin1.mast) for bin1 in self._values)

    @property
    def uncertainty(self) -> float:
        return self._calculate_uncertainty(self._values)

    def add_bin(self, bin_information: BinInformation):
        with self._lock:
            self._values.append(bin_information)

    def per_turbine_uncertainty(self, turbine: Turbine) -> float:
        return self._calculate_uncertainty([x for x in self._values if x.turbine == turbine]) 