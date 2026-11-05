"""Module for import .csv files"""

import csv


class Reader:
    """csv reader class"""
    def __init__(self, separator: str = ",", encoding: str = "UTF-8"):
        self.data = []
        self.title = []

        self.separator = separator
        self.encoding = encoding

    def read(self, csv_dir: str):
        """read csv file by direction"""
        with open(csv_dir, encoding=self.encoding, mode="r") as file:
            data = csv.reader(file, delimiter=self.separator)

            for num, row in enumerate(data):
                if num == 0:
                    self.title = row

                elif len(self.title) == len(row):
                    self.data.append(row)

                else:
                    raise ValueError(f"At {num} row fields count is {len(row)}, \
                                     but must be a {len(self.title)}")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __iter__(self):
        return iter(self.data)


if __name__ == "__main__":
    raeder = Reader()
