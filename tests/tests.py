"""Tests for Reader class"""

import os
import tempfile
import unittest

from src.main import Reader


class TestReader(unittest.TestCase):
    """Tests for csv Reader"""

    def setUp(self):
        """make temp folder for test files"""
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "test.csv")

    def tearDown(self):
        """remove temp folder"""
        self.folder.cleanup()

    def write_file(self, text):
        """write text to test file"""
        with open(self.path, "w", encoding="UTF-8", newline="") as file:
            file.write(text)

    def test_read(self):
        """title and rows are read correctly"""
        self.write_file("id,name\n1,apple\n2,pear\n")
        reader = Reader()
        reader.read(self.path)

        self.assertEqual(reader.title, ["id", "name"])
        self.assertEqual(reader.data, [["1", "apple"], ["2", "pear"]])

    def test_len(self):
        """len returns rows count without title"""
        self.write_file("id,name\n1,apple\n2,pear\n")
        reader = Reader()
        reader.read(self.path)

        self.assertEqual(len(reader), 2)

    def test_getitem(self):
        """get row by index"""
        self.write_file("id,name\n1,apple\n2,pear\n")
        reader = Reader()
        reader.read(self.path)

        self.assertEqual(reader[0], ["1", "apple"])
        self.assertEqual(reader[1], ["2", "pear"])

    def test_iter(self):
        """reader works in for loop"""
        self.write_file("id,name\n1,apple\n2,pear\n")
        reader = Reader()
        reader.read(self.path)

        rows = []
        for row in reader:
            rows.append(row)

        self.assertEqual(rows, [["1", "apple"], ["2", "pear"]])

    def test_separator(self):
        """reader works with other separator"""
        self.write_file("id;name\n1;apple\n")
        reader = Reader(separator=";")
        reader.read(self.path)

        self.assertEqual(reader.title, ["id", "name"])
        self.assertEqual(reader[0], ["1", "apple"])

    def test_wrong_fields_count(self):
        """error if row has wrong fields count"""
        self.write_file("id,name\n1,apple,10\n")
        reader = Reader()

        with self.assertRaises(ValueError):
            reader.read(self.path)

    def test_file_not_found(self):
        """error if file does not exist"""
        reader = Reader()

        with self.assertRaises(FileNotFoundError):
            reader.read("no_such_file.csv")


if __name__ == "__main__":
    unittest.main()
