import os.path


class fehlerkorrektur:
    def __init__(self):
        path2 = os.path.join(os.path.dirname(__file__), "data")
        with open(path2 + '/USA-Prae.csv', 'r') as file:
            example_president = []
            example_start = []
            example_end = []
            data_president = []
            data_start = []
            data_end = []
            for idx, line in enumerate(file, start=1):
                row = line.split(';')
                if idx < 6:
                    example_president.append(row[0])
                    example_start.append(row[1])
                    example_end.append(row[2].strip())
                else:
                    data_president.append(row[0])
                    data_start.append(row[1])
                    data_end.append(row[2].strip())
        self.example_president = example_president
        self.example_start = example_start
        self.example_end = example_end
        self.data_president = data_president
        self.data_start = data_start
        self.data_end = data_end
