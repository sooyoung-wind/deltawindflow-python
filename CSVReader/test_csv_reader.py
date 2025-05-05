import unittest
import io
from CSVReader.csv_reader import CSVReader, DataNotRectangularException, ParsingException

class TestCSVReader(unittest.TestCase):
    def test_basic_csv(self):
        csv = """Column1,Column2,Column3\nData1-1,Data2-1,Data3-1\nData1-2,Data2-2,Data3-2\nData1-3,Data2-3,Data3-3\n"""
        reader = CSVReader(io.StringIO(csv))
        self.assertEqual(reader.row_count, 3)
        self.assertEqual(reader.headers, ["Column1", "Column2", "Column3"])
        self.assertEqual(reader[0], ["Data1-1", "Data1-2", "Data1-3"])
        self.assertEqual(reader["Column2"], ["Data2-1", "Data2-2", "Data2-3"])

    def test_type_conversion(self):
        csv = """A,B,C\n1,2.5,2020-01-01\n2,3.5,2020-01-02\n3,4.5,2020-01-03\n"""
        reader = CSVReader(io.StringIO(csv))
        self.assertEqual(reader.get_int_list("A"), [1,2,3])
        self.assertEqual(reader.get_double_list("B"), [2.5,3.5,4.5])
        self.assertEqual([d.strftime('%Y-%m-%d') for d in reader.get_datetime_list("C")], ["2020-01-01","2020-01-02","2020-01-03"])

    def test_blank_line(self):
        csv = """A,B\n1,2\n3,4\n\n5,6\n"""
        reader = CSVReader(io.StringIO(csv))
        self.assertEqual(reader.row_count, 3)
        self.assertEqual(reader["A"], ["1","3","5"])

    def test_data_not_rectangular(self):
        csv = """A,B\n1,2\n3\n5,6\n"""
        with self.assertRaises(DataNotRectangularException):
            CSVReader(io.StringIO(csv))

    def test_parsing_exception(self):
        csv = """A\n1\nabc\n3\n"""
        reader = CSVReader(io.StringIO(csv))
        with self.assertRaises(ParsingException):
            reader.get_int_list("A")

    def test_custom_type(self):
        csv = """A\n1\n2\n3\n"""
        reader = CSVReader(io.StringIO(csv))
        def parse_double(s):
            return float(s) * 2
        self.assertEqual(reader.get_custom_type_list(parse_double, "A"), [2.0, 4.0, 6.0])

if __name__ == '__main__':
    unittest.main() 