
if __name__ == "__main__":
    file = open("data/kddcup.data_10_percent_corrected")
    classification = {}
    count = 0
    for line in file.readlines():
        splited = line.split(",")
        count = count + 1
        key = splited[-1].strip().replace('.','')
        if classification.get(key) is None:
            classification[key] = 1
        else:
            classification[key] = classification[key] + 1

    print("total:", count)
    for (k,v) in classification.items():
        print("{0},{1},{2}".format(k, v, float(v)/count))