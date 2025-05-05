import unittest
from Clerc2011.turbine import Turbine
from Clerc2011.mast import Mast
from Clerc2011.bin_information import BinInformation
from Clerc2011.mast_weighting import MastWeighting
from Clerc2011.topo_uncertainty_calculator import TopoUncertaintyCalculator

class TestClerc2011(unittest.TestCase):
    def test_turbine_and_mast_equality(self):
        t1 = Turbine(1.0, 2.0)
        t2 = Turbine(1.0, 2.0)
        t3 = Turbine(2.0, 3.0)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)
        m1 = Mast(1.0, 2.0)
        m2 = Mast(1.0, 2.0)
        m3 = Mast(2.0, 3.0)
        self.assertEqual(m1, m2)
        self.assertNotEqual(m1, m3)

    def test_bin_information_equality(self):
        t = Turbine(1.0, 2.0)
        m = Mast(3.0, 4.0)
        b1 = BinInformation(t, m, 10, 1.2, 0.5, 100)
        b2 = BinInformation(t, m, 10, 1.2, 0.5, 100)
        b3 = BinInformation(t, m, 20, 1.2, 0.5, 100)
        self.assertEqual(b1, b2)
        self.assertNotEqual(b1, b3)

    def test_topo_uncertainty_calculator(self):
        t = Turbine(0, 0)
        m = Mast(1, 0)
        mast_weighting = MastWeighting(m, 1.0)
        mast_weightings = {t: [mast_weighting]}
        calc = TopoUncertaintyCalculator(
            lamda=0.5,
            length_scale=1.0,
            a=0.2,
            mast_weightings=mast_weightings,
            offshore=False
        )
        bin_info = BinInformation(t, m, 0, 1.1, 1.0, 10.0)
        calc.add_bin(bin_info)
        self.assertGreater(calc.energy, 0)
        self.assertGreaterEqual(calc.uncertainty, 0)
        self.assertGreaterEqual(calc.per_turbine_uncertainty(t), 0)

if __name__ == '__main__':
    unittest.main() 