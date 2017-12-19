# generate csv files for graph


def extract_accuracy_to_file(output_path, files=[]):
    with open(output_path, 'w') as write_f:
        # write head first.
        write_f.write("Time,")
        results = []
        for f in files:
            write_f.write(f[0])
            write_f.write(",")
            results.append(extract_accuracy_from_file(f[1]))
        write_f.write("\n")
        for i in range(2000,102000,2000):
            id = str(i)
            write_f.write(id)
            write_f.write(",")
            for result in results:
                write_f.write(result[id])
                write_f.write(",")
            write_f.write("\n")


def extract_accuracy_from_file(f):
    result = {}
    with open(f) as input_f:
        for line in input_f.readlines():
            if line.startswith("accuracy: "):
                arr = line.split(",")
                result[arr[1].split(":")[1].strip()] = arr[0].split(":")[1]
    return result


def extract_time_from_file(f):
    result = {}
    with open(f) as input_f:
        for line in input_f.readlines():
            if line.startswith("time: "):
                arr = line.split(",")
                result[arr[1].split(":")[1].strip()] = arr[0].split(":")[1]
    return result


def extract_time_to_file(output_path, files=[]):
    with open(output_path, 'w') as write_f:
        # write head first.
        write_f.write("Time,")
        results = []
        for f in files:
            write_f.write(f[0])
            write_f.write(",")
            results.append(extract_time_from_file(f[1]))
        write_f.write("\n")
        for i in range(2000,102000,2000):
            id = str(i)
            write_f.write(id)
            write_f.write(",")
            for result in results:
                write_f.write(result[id])
                write_f.write(",")
            write_f.write("\n")

def extract_accuracy_graph():
    extract_accuracy_to_file("../result/csv_compare_accuracy.csv",
                             [
                                 ["Knn200", "../result/generated.knn.200-k1"],
                                 ["Knn100", "../result/generated.knn.100-k1"],
                                 ["ECSMiner", "../result/generated_ecsminer-no-novel"],
                                 ["AlphaKmeans", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"]
                             ])

def extract_time_graph():
    extract_time_to_file("../result/csv_compare_time.csv",
                             [
                                 ["Knn200", "../result/generated.knn.200-k1"],
                                 ["Knn100", "../result/generated.knn.100-k1"],
                                 ["ECSMiner", "../result/generated_ecsminer-no-novel"],
                                 ["AlphaKmeans", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"]
                             ])


if __name__ == '__main__':
    # extract_accuracy_graph()
    extract_time_graph()
