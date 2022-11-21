import unittest
import sys
import os
import pandas as pd
from pathlib import Path

sys.path.append(rf"{Path(__file__).parent.parent}\src")
import push_pull_local as loc 

class test_load_dictionary_from_json(unittest.TestCase):

    def setUp(self) -> None:
        self.data_path = rf"{os.path.dirname(__file__)}\test_files"
        self.dict_file = rf"{self.data_path}\dict.json"

    
    def test_dict_correctly_loads(self):
        actual_dict = loc.load_dictionary_from_json(self.dict_file, [])
        expected_dict = {"language":"python", "repo":"push_pull", "source":"local"}
        self.assertEqual(actual_dict, expected_dict, "dicts not equal")


    def test_dict_ignore_list_correctly_loads(self):
        actual_dict = loc.load_dictionary_from_json(self.dict_file, ["repo"])
        expected_dict = {"language":"python", "source":"local"}
        self.assertEqual(actual_dict, expected_dict, "dicts not equal")


    def test_no_file_returns_None(self):
        file = rf"{self.data_path}\dict1.json"
        actual_dict = loc.load_dictionary_from_json(file, [])
        expected_dict = None
        self.assertEqual(actual_dict, expected_dict, "dicts not equal")


class test_append_dictionary_to_csv(unittest.TestCase):

    def setUp(self) -> None:
        self.data_path = rf"{os.path.dirname(__file__)}\test_files"
        self.dict_file = rf"{self.data_path}\dict.json"


    def test_dict_correctly_uploads(self):
        dict = loc.load_dictionary_from_json(self.dict_file, ["repo"])
        dict_csv = rf"{self.data_path}\dict.csv"
        dict_dataframe = pd.DataFrame({'language': ["C++"], 'source': ["influx"]})
        dict_dataframe.to_csv(dict_csv, index = False)
        loc.append_dictionary_to_csv(dict_csv, dict)

        actual_data = pd.read_csv(dict_csv).to_string()
        expected_data = pd.DataFrame({'language': ["C++", "python"], 'source': ["influx", "local"]}).to_string()

        self.assertEqual(actual_data, expected_data, "dataframes not equal")


    def test_dict_bad_columns_still_uploads(self):
        dict = loc.load_dictionary_from_json(self.dict_file, ["repo"])
        dict_csv = rf"{self.data_path}\dict.csv"
        dict_dataframe = pd.DataFrame({'year': [2022], 'source': ["influx"]})
        dict_dataframe.to_csv(dict_csv, index = False)
        loc.append_dictionary_to_csv(dict_csv, dict)

        actual_data = pd.read_csv(dict_csv).to_string()
        expected_data = pd.DataFrame({'year': [2022, "python"], 'source': ["influx", "local"]}).to_string()

        self.assertEqual(actual_data, expected_data, "dataframes not equal")



if __name__ == '__main__':
    unittest.main()