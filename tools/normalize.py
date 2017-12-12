# some normalization methods.
import analysis
import names
import iotool

default_cache_file_meta_min_max = "../data/cached_normalize_meta_min_max"


def read_min_max(input_name):
    att_values_map = analysis.value_ranges(input_name)
    att_type_map = names.att_type_map
    att_min_max_map = dict(map(
        lambda (k,v): (k, [v[0],v[-1]] if att_type_map.get(k) == "continuous" else v),
        att_values_map.iteritems()))
    return att_min_max_map


def get_min_max(input_name):
    cache_path = "{0}-{1}".format(default_cache_file_meta_min_max, input_name.split("/")[-1])
    return iotool.cached_method(cache_path, read_min_max, input_name)


def min_max_normalize(input_name, output_suffix):
    att_minmax_map = get_min_max(input_name)
    att_type_map = names.att_type_map
    att_list = names.name_list

    output_file_name = "{0}.{1}".format(input_name, output_suffix)
    with open(input_name) as input_f, open(output_file_name,"w") as output_f:
        for line in input_f.readlines():
            val_arr = line.replace(".","").strip().split(",")
            for (index, val) in enumerate(val_arr[:-1]):
                if att_type_map.get(att_list[index]) == "continuous":
                    att = att_list[index]
                    try:
                        normalized = (float(val) - att_minmax_map.get(att)[0]) /\
                                 (att_minmax_map.get(att)[-1] - att_minmax_map.get(att)[0])
                        output_f.write("{0},".format(normalized))
                    except ZeroDivisionError:
                        # ignore this attribute.
                        output_f.write("0,")
                else:
                    output_f.write("{0},".format(val))
            output_f.write("\n")


if __name__ == "__main__":
    min_max_normalize("../data/kddcup.data_10_percent_corrected", "minmax")