# a tool to access the dataset

import names


class DataSet:
    """
    To make reading dataset easier.
    """

    def __init__(self, input_name, size = None):
        self.input_f = open(input_name)
        self.name_list = names.name_list
        self.type_dict = names.att_type_map
        self.size = size
        self.counter = 0

    def __del__(self):
        if not self.input_f.closed:
            self.input_f.close()

    def __iter__(self):
        return self

    def next(self):
        line = self.input_f.readline()
        if line is None or self.counter == self.size or len(line) == 0:
            raise StopIteration
        else:
            self.counter += 1
            split = line.strip().replace(".", "").split(",")
            values = []
            for index, att in enumerate(self.name_list):
                try:
                    if self.type_dict.get(att) == "continuous":
                        values.append(float(split[index].strip()))
                    else:
                        values.append(split[index].strip())
                except ValueError, e:
                    print("Error", e)
                    print(split)
                    print(index)
            # append label
            values.append(split[-1])
            return values


if __name__ == '__main__':
    for item in DataSet("../data/kddcup.data_10_percent_corrected"):
        pass
    # for item in DataSet("../data/kddcup.data_10_percent_corrected", 10):
    #     print(item)