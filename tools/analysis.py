# some analysis about the dataset

import names


def value_ranges(input_f):
    file = open(input_f)
    distinct_values_map = {}
    name_list = names.name_list
    type_dict = names.att_type_map
    for line in file.readlines():
        splitted = line.strip().replace(".","").split(",")
        for index, att in enumerate(name_list):
            distinct_values = distinct_values_map.get(att)
            if distinct_values is None:
                distinct_values = []
                distinct_values_map[att] = distinct_values
            value = None
            if type_dict[att] == "continuous":
                # convert to float
                value = float(splitted[index])
            else :
                value = splitted[index]
            # add
            if value not in distinct_values:
                distinct_values.append(value)
    file.close()

    # sort the values.
    for (att,values) in distinct_values_map.items():
        sv = sorted(values)
        if type_dict[att] == "continuous":
            print("{0}, {1} to {2}".format(att, sv[0], sv[-1]))
        else :
            print("{0}, {1}".format(att, sv))

if __name__ == "__main__":
    value_ranges("../data/kddcup.data_10_percent_corrected")