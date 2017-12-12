import json
import os

def persist_to_file(output_file_name, obj):
    """
    persist a object to output file.
    :param distinct_values_map:
    :param output_file_name:
    :return:
    """
    with open(output_file_name, "w") as output_file:
        json.dump(obj, output_file)


def read_from_file(input_file_name):
    """
    read the object from a file.
    :param input_file_name:
    :return:
    """
    with open(input_file_name, "r") as input_file:
        return json.load(input_file)


def cached_method(cache_file, init_method, *args):
    """
    a decorator to make cache easier
    :param cache_file:
    :param init_method:
    :return:
    """
    if os.path.exists(cache_file):
        return read_from_file(cache_file)
    else:
        v = init_method(*args)
        persist_to_file(cache_file, v)
        return v