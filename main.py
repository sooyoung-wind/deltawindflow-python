import sys
import os
from CSVReader.csv_reader import CSVReader
from Clerc2011.mast import Mast
from Clerc2011.turbine import Turbine
from Clerc2011.mast_weighting import MastWeighting
from Clerc2011.bin_information import BinInformation
from Clerc2011.topo_uncertainty_calculator import TopoUncertaintyCalculator

def get_index(ids, id_):
    for i, v in enumerate(ids):
        if v == id_:
            return i
    return -1

def main(mast_csv, turbine_csv, bin_csv):
    mast_reader = CSVReader(mast_csv)
    masts = []
    mast_ids = []
    for i in range(mast_reader.row_count):
        masts.append(Mast(float(mast_reader["MastX"][i]), float(mast_reader["MastY"][i])))
        mast_ids.append(int(mast_reader["MastID"][i]))

    turbine_reader = CSVReader(turbine_csv)
    turbines = []
    turbine_ids = []
    weightings = {}
    for i in range(turbine_reader.row_count):
        turbines.append(Turbine(float(turbine_reader["TurbineX"][i]), float(turbine_reader["TurbineY"][i])))
        turbine_ids.append(int(turbine_reader["TurbineID"][i]))
        weights = []
        for j, mast_id in enumerate(mast_ids):
            weight = float(turbine_reader[f"Mast{mast_id}Weight"][i])
            weights.append(MastWeighting(masts[j], weight))
        weightings[turbines[i]] = weights

    calculator = TopoUncertaintyCalculator(0.1, 1000, 0.5, weightings, False)

    bin_reader = CSVReader(bin_csv)
    for i in range(bin_reader.row_count):
        mast_id = int(bin_reader["MastID"][i])
        turbine_id = int(bin_reader["TurbineID"][i])
        mast_index = get_index(mast_ids, mast_id)
        turbine_index = get_index(turbine_ids, turbine_id)
        calculator.add_bin(BinInformation(
            turbine=turbines[turbine_index],
            mast=masts[mast_index],
            direction=float(bin_reader["Direction"][i]),
            speedup=float(bin_reader["SpeedUp"][i]),
            sensitivity_factor=float(bin_reader["Sensitivity"][i]),
            bin_energy=float(bin_reader["Energy"][i])
        ))

    print()
    print(f"Energy:                  {calculator.energy:0.02f}")
    print(f"Flow Model Uncertainty:  {calculator.uncertainty:0.02f}")

if __name__ == "__main__":
    # Example 폴더의 파일을 기본값으로 사용
    base = os.path.join(os.path.dirname(__file__), "Example")
    mast_csv = os.path.join(base, "MastLocations.csv")
    turbine_csv = os.path.join(base, "TurbineLocationsAndMastWeights.csv")
    bin_csv = os.path.join(base, "BinInformation.csv")
    main(mast_csv, turbine_csv, bin_csv) 
