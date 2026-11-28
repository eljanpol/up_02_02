"""Unit tests for src.main.Reader"""

import os
import tempfile
import unittest

from src.main import Reader


class ReaderTests(unittest.TestCase):
    """Tests for csv Reader class"""

    def setUp(self):
        """create temporary directory for csv files"""
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp_dir = tmp.name

    def make_csv(self, content: str, encoding: str = "UTF-8") -> str:
        """write content to temporary csv file and return its path"""
        path = os.path.join(self.tmp_dir, "test.csv")
        with open(path, mode="w", encoding=encoding, newline="") as file:
            file.write(content)
        return path

    def test_default_params(self):
        """new Reader has default separator, encoding and empty data"""
        reader = Reader()

        self.assertEqual(reader.separator, ",")
        self.assertEqual(reader.encoding, "UTF-8")
        self.assertEqual(reader.title, [])
        self.assertEqual(reader.data, [])
        self.assertEqual(len(reader), 0)

    def test_read_title_and_rows(self):
        """first row goes to title, other rows go to data"""
        path = self.make_csv("id,name,price\n1,apple,10\n2,pear,20\n")
        reader = Reader()

        reader.read(path)

        self.assertEqual(reader.title, ["id", "name", "price"])
        self.assertEqual(reader.data, [["1", "apple", "10"],
                                       ["2", "pear", "20"]])

    def test_len(self):
        """len() returns rows count without title"""
        path = self.make_csv("a,b\n1,2\n3,4\n5,6\n")
        reader = Reader()

        reader.read(path)

        self.assertEqual(len(reader), 3)

    def test_getitem(self):
        """indexing returns row by its number"""
        path = self.make_csv("a,b\n1,2\n3,4\n")
        reader = Reader()

        reader.read(path)

        self.assertEqual(reader[0], ["1", "2"])
        self.assertEqual(reader[1], ["3", "4"])
        self.assertEqual(reader[-1], ["3", "4"])

    def test_getitem_out_of_range(self):
        """indexing outside of data raises IndexError"""
        path = self.make_csv("a,b\n1,2\n")
        reader = Reader()

        reader.read(path)

        with self.assertRaises(IndexError):
            _ = reader[5]

    def test_iter(self):
        """Reader can be used in for loop"""
        path = self.make_csv("a,b\n1,2\n3,4\n")
        reader = Reader()

        reader.read(path)

        self.assertEqual(list(reader), [["1", "2"], ["3", "4"]])

    def test_custom_separator(self):
        """Reader splits rows by custom separator"""
        path = self.make_csv("a;b;c\n1;2;3\n")
        reader = Reader(separator=";")

        reader.read(path)

        self.assertEqual(reader.title, ["a", "b", "c"])
        self.assertEqual(reader[0], ["1", "2", "3"])

    def test_custom_encoding(self):
        """Reader reads file in custom encoding"""
        path = self.make_csv("товар,цена\nяблоко,10\n", encoding="cp1251")
        reader = Reader(encoding="cp1251")

        reader.read(path)

        self.assertEqual(reader.title, ["товар", "цена"])
        self.assertEqual(reader[0], ["яблоко", "10"])

    def test_quoted_field_with_separator(self):
        """separator inside quotes is not a field delimiter"""
        path = self.make_csv('id,name\n1,"Smith, John"\n')
        reader = Reader()

        reader.read(path)

        self.assertEqual(reader[0], ["1", "Smith, John"])

    def test_only_title(self):
        """file with only title has no data rows"""
        path = self.make_csv("a,b,c\n")
        reader = Reader()

        reader.read(path)

        self.assertEqual(reader.title, ["a", "b", "c"])
        self.assertEqual(len(reader), 0)

    def test_empty_file(self):
        """empty file gives empty title and data"""
        path = self.make_csv("")
        reader = Reader()

        reader.read(path)

        self.assertEqual(reader.title, [])
        self.assertEqual(len(reader), 0)

    def test_row_with_extra_field(self):
        """row with more fields than title raises ValueError"""
        path = self.make_csv("a,b\n1,2\n3,4,5\n")
        reader = Reader()

        with self.assertRaises(ValueError) as context:
            reader.read(path)

        self.assertIn("At 2 row fields count is 3", str(context.exception))

    def test_row_with_missing_field(self):
        """row with fewer fields than title raises ValueError"""
        path = self.make_csv("a,b,c\n1,2\n")
        reader = Reader()

        with self.assertRaises(ValueError) as context:
            reader.read(path)

        self.assertIn("At 1 row fields count is 2", str(context.exception))

    def test_file_not_found(self):
        """reading missing file raises FileNotFoundError"""
        reader = Reader()
        path = os.path.join(self.tmp_dir, "missing.csv")

        with self.assertRaises(FileNotFoundError):
            reader.read(path)


if __name__ == "__main__":
    unittest.main()
