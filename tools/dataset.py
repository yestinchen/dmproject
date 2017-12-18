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
            split = line.strip().split(",")
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


class NumericSet:
    """
    data set contains all numeric values.
    Just remove all the categorical values.
    """
    def __init__(self, dataset, keepcol = []):
        self.dataset = dataset
        self.keepcol = keepcol

    def __iter__(self):
        return self

    def next(self):
        record = self.dataset.next()
        if record is None:
            raise StopIteration
        else:
            return numeric_filter(record, self.keepcol)


def numeric_filter(record, keep_col=[]):
        newrecord = []
        for (index, value) in enumerate(record):
            if index in keep_col or not isinstance(value, str):
                newrecord.append(value)
        return newrecord


if __name__ == '__main__':
    # for item in DataSet("../data/kddcup.data_10_percent_corrected"):
    #     pass
    for item in names.name_list:
        print(item, names.att_type_map[item])
    for item in NumericSet(DataSet("../data/kddcup.data_10_percent_corrected.minmax.shuffled", 10), [41]):
        print(item)