import os
import csv


class My_CSV:
    """
    Class to manipulate my CSV's files
    """

    def write_file(self, path: str, filename: str, header: list,
                   data: list) -> None:
        filename = filename if filename.endswith('.csv') else filename + '.csv'

        path = os.path.join(path, filename)

        with open(path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            writer.writerow(header)

            writer.writerows(data)

    def read_file(self, path) -> str:
        text = ''
        with open(path, encoding="utf8") as f:
            reader = csv.reader(f)

            next(reader)

            text = reader

        return text
