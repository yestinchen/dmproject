# some analysis about the dataset

import names
import iotool
import os

default_cache_file_prefix = "../data/cached_analysis_value_ranges"


def value_ranges(input_f):
    cache_path = "{0}-{1}".format(default_cache_file_prefix, input_f.split("/")[-1])
    return iotool.cached_method(cache_path, value_ranges_read, input_f)


def value_ranges_read(input_f):
    """
    Get value ranges for each attributes
    :param input_f: input file
    :return: a dict contains (attribute_name,[ordered value list])
    """

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

    return dict(map(lambda (k,v) : (k, sorted(v)), distinct_values_map.iteritems()))


def print_att_map(distinct_values_map):
    """
    Print the map to the screen
    :param distinct_values_map: input sorted map
    :return: None
    """
    type_dict = names.att_type_map
    # sort the values.
    for (att,values) in distinct_values_map.items():
        sv = sorted(values)
        if type_dict[att] == "continuous":
            print("{0}, {1} to {2}".format(att, sv[0], sv[-1]))
        else :
            print("{0}, {1}".format(att, sv))


if __name__ == "__main__":
    print_att_map(value_ranges("../data/kddcup.data_10_percent_corrected"))