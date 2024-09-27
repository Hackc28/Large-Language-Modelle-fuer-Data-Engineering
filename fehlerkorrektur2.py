import os.path


class fehlerkorrektur_transformation:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "data")
        with open(path + '/Telefon.csv', 'r') as file:
            example = []
            example_solution = []
            data = []
            data_solution = []
            for idx, line in enumerate(file, start=1):
                row = line.split(';')
                if idx < 11:
                    example.append(row[0])
                    example_solution.append(row[1].strip())
                else:
                    data.append(row[0])
                    data_solution.append(row[1].strip())
        self.example = example
        self.example_solution = example_solution
        self.data = data
        self.data_solution = data_solution
