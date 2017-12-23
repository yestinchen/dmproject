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

def extract_accuracy_graph_w():
    extract_accuracy_to_file("../result/csv_w_accuracy.csv",
                             [
                                 ["w=100", "../result/generated.alpha.kmeans.100.knn_k1.cluster_n50.model_n5"],
                                 ["w=500", "../result/generated.alpha.kmeans.500.knn_k1.cluster_n50.model_n5"],
                                 ["w=1000", "../result/generated.alpha.kmeans.1000.knn_k1.cluster_n50.model_n5"],
                                 ["w=1500", "../result/generated.alpha.kmeans.1500.knn_k1.cluster_n50.model_n5"],
                                 ["w=2000", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"],
                                 ["w=2500", "../result/generated.alpha.kmeans.2500.knn_k1.cluster_n50.model_n5"]
                             ])

def extract_time_graph_w():
    extract_time_to_file("../result/csv_w_time.csv",
                             [
                                 ["w=100", "../result/generated.alpha.kmeans.100.knn_k1.cluster_n50.model_n5"],
                                 ["w=500", "../result/generated.alpha.kmeans.500.knn_k1.cluster_n50.model_n5"],
                                 ["w=1000", "../result/generated.alpha.kmeans.1000.knn_k1.cluster_n50.model_n5"],
                                 ["w=1500", "../result/generated.alpha.kmeans.1500.knn_k1.cluster_n50.model_n5"],
                                 ["w=2000", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"],
                                 ["w=2500", "../result/generated.alpha.kmeans.2500.knn_k1.cluster_n50.model_n5"]
                             ])

def extract_time_graph():
    extract_time_to_file("../result/csv_compare_time.csv",
                             [
                                 ["Knn200", "../result/generated.knn.200-k1"],
                                 ["Knn100", "../result/generated.knn.100-k1"],
                                 ["ECSMiner", "../result/generated_ecsminer-no-novel"],
                                 ["AlphaKmeans", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"]
                             ])

def extract_accuracy_graph_c():
    extract_accuracy_to_file("../result/csv_c_accuracy.csv",
                             [
                                 ["c=10", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n10.model_n5"],
                                 ["c=20", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n20.model_n5"],
                                 ["c=30", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n30.model_n5"],
                                 ["c=40", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n40.model_n5"],
                                 ["c=50", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"],
                                 ["c=60", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n60.model_n5"]
                             ])

def extract_time_graph_c():
    extract_time_to_file("../result/csv_c_time.csv",
                             [
                                 ["c=10", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n10.model_n5"],
                                 ["c=20", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n20.model_n5"],
                                 ["c=30", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n30.model_n5"],
                                 ["c=40", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n40.model_n5"],
                                 ["c=50", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"],
                                 ["c=60", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n60.model_n5"]
                             ])

def extract_accuracy_graph_k():
    extract_accuracy_to_file("../result/csv_k_accuracy.csv",
                             [
                                 ["k=1", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"],
                                 ["k=2", "../result/generated.alpha.kmeans.2000.knn_k2.cluster_n50.model_n5"],
                                 ["k=3", "../result/generated.alpha.kmeans.2000.knn_k3.cluster_n50.model_n5"],
                                 ["k=4", "../result/generated.alpha.kmeans.2000.knn_k4.cluster_n50.model_n5"],
                                 ["k=5", "../result/generated.alpha.kmeans.2000.knn_k5.cluster_n50.model_n5"],
                                 ["k=6", "../result/generated.alpha.kmeans.2000.knn_k6.cluster_n50.model_n5"]
                             ])
def extract_time_graph_k():
    extract_time_to_file("../result/csv_k_time.csv",
                             [
                                 ["k=1", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"],
                                 ["k=2", "../result/generated.alpha.kmeans.2000.knn_k2.cluster_n50.model_n5"],
                                 ["k=3", "../result/generated.alpha.kmeans.2000.knn_k3.cluster_n50.model_n5"],
                                 ["k=4", "../result/generated.alpha.kmeans.2000.knn_k4.cluster_n50.model_n5"],
                                 ["k=5", "../result/generated.alpha.kmeans.2000.knn_k5.cluster_n50.model_n5"],
                                 ["k=6", "../result/generated.alpha.kmeans.2000.knn_k6.cluster_n50.model_n5"]
                             ])
def extract_accuracy_graph_N():
    extract_accuracy_to_file("../result/csv_N_accuracy.csv",
                             [
                                 ["N=1", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n1"],
                                 ["N=2", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n2"],
                                 ["N=3", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n3"],
                                 ["N=4", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n4"],
                                 ["N=5", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"],
                                 ["N=6", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n6"]
                             ])
def extract_time_graph_N():
    extract_time_to_file("../result/csv_N_time.csv",
                             [
                                 ["N=1", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n1"],
                                 ["N=2", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n2"],
                                 ["N=3", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n3"],
                                 ["N=4", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n4"],
                                 ["N=5", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50"],
                                 ["N=6", "../result/generated.alpha.kmeans.2000.knn_k1.cluster_n50.model_n6"]
                             ])
if __name__ == '__main__':
    # extract_accuracy_graph()
    # extract_time_graph()
    # extract_accuracy_graph_w()
    # extract_time_graph_w()
    # extract_accuracy_graph_c()
    # extract_time_graph_c()
    # extract_accuracy_graph_k()
    extract_time_graph_k()
    # extract_accuracy_graph_N()
    # extract_time_graph_N()
