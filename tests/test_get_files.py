import unittest
import sys
import os
import os.path
from pathlib import Path

sys.path.append(rf"{Path(__file__).parent.parent}\src")
import push_pull_local as loc 

class test_get_file_list_containing_strings(unittest.TestCase):

    def setUp(self) -> None:
        self.data_path = rf"{os.path.dirname(__file__)}\test_files"
    

    def test_one_string_returns_correct_list(self):
        str_list = ["file"]
        actual_files = loc.get_file_list_containing_strings(str_list, self.data_path)
        expected_files = ["file1.csv", "file2.csv", "file3.csv"]
        actual_files.sort()
        expected_files.sort()
        self.assertEqual(actual_files, expected_files, "lists not equal")


    def test_multiple_strings_returns_correct_list(self):
        str_list = ["file", "1"]
        actual_files = loc.get_file_list_containing_strings(str_list, self.data_path)
        expected_files = ["file1.csv", "file2.csv", "file3.csv", "table1.csv"]
        actual_files.sort()
        expected_files.sort()
        self.assertCountEqual(actual_files, expected_files, "lists not equal")


    def test_no_string_returns_empty_list(self):
        actual_files = loc.get_file_list_containing_strings([], self.data_path)
        expected_files = []
        self.assertEqual(actual_files, expected_files, "actual list not empty")


    def test_no_files_returns_empty_list(self):
        str_list = ["hi"]
        actual_files = loc.get_file_list_containing_strings(str_list, self.data_path)
        expected_files = []
        self.assertEqual(actual_files, expected_files, "actual list not empty")


class test_get_most_recent_files(unittest.TestCase):

    def setUp(self) -> None:
        self.data_path = rf"{os.path.dirname(__file__)}\test_files"
    

    def test_extension_returns_correct_file(self):
        file_extension = ".csv"
        actual_file = loc.get_most_recent_file(self.data_path, file_extension)
        expected_file = fr"{self.data_path}\dict.csv"
        self.assertEqual(actual_file, expected_file, "lists not equal")


    def test_no_files_returns_None(self):
        file_extension = ".txt"
        actual_file = loc.get_most_recent_file(self.data_path, file_extension)
        expected_file = None
        self.assertEqual(actual_file, expected_file, "lists not equal")

if __name__ == '__main__':
    unittest.main()