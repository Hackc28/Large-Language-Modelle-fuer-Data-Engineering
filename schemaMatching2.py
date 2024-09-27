import os.path


class schema_matching2:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "data")
        with open(path + '/Schema-Match.csv', 'r') as file:
            example_column_1 = []
            example_column_2 = []
            example_solution = []
            data_column_1 = []
            data_column_2 = []
            data_solution = []
            for idx, line in enumerate(file, start=1):
                row = line.split(';')
                if idx < 8:
                    example_column_1.append(row[0])
                    example_column_2.append(row[1])
                    example_solution.append(row[2].strip())
                else:
                    data_column_1.append(row[0])
                    data_column_2.append(row[1])
                    data_solution.append(row[2].strip())
        self.example_column_1 = example_column_1
        self.example_column_2 = example_column_2
        self.example_solution = example_solution
        self.data_column_1 = data_column_1
        self.data_column_2 = data_column_2
        self.data_solution = data_solution
