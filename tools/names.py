# a utility to read the input types.

name_list = None
att_type_map = None


def init(f_name):
    global name_list, att_type_map
    name_list = []
    att_type_map = {}
    f = open(f_name)
    for line in f.readlines():
        arr = line.split(":")
        if len(arr) == 2:
            name_list.append(arr[0])
            att_type_map[arr[0]] = arr[1].strip()[:-1]


if __name__ == "names":
    init("../data/kddcup.names")
