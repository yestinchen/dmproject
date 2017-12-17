# random sample.
import random


if __name__ == '__main__':
    with open("../data/kddcup.data_10_percent_corrected.minmax") as open_f:
        with open("../data/kddcup.data_10_percent_corrected.minmax.shuffled", "w") as write_f:
            list = open_f.readlines()
            random.shuffle(list)
            for line in list:
                write_f.write(line)
