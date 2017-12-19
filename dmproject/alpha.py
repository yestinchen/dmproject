# solution a

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import numpy
from tools.dataset import DataSet, NumericSet, numeric_filter
from reporter import AccuracyBufferedReporter

class Alpha:
    """
    plan a
    """

    def __init__(self, max_points_num = 10, knn_k = 1):
        self.Time = 0
        self.reporter = AccuracyBufferedReporter()
        # label, model
        self.models = {}
        self.max_points_num = max_points_num
        self.Knn_K = knn_k

    def classify_using_mean_distance(self, query):
        """
        this method performs not so good. Maybe because it will get influenced by outliers in the cluster.
        :param query:
        :return:
        """
        mean_distance = {}
        for label, points in self.models.items():
            distance_matrix = euclidean_distances([query], points)
            total_distance = 0.0
            for d in distance_matrix[0]:
                total_distance += d
            mean_distance[label] = total_distance / len(points)
        sorted_distance = sorted(mean_distance.items(), key=lambda x: x[1])
        print(sorted_distance)
        return None if len(sorted_distance) == 0 else sorted_distance[0][0]

    def classify_using_min_distance(self, query):
        min_distance = []
        for label, points in self.models.items():
            distance_matrix = euclidean_distances([query], points)
            ordered_matrix = sorted(distance_matrix[0])
            mapped_matrix = map(lambda x: [label, x],
                                ordered_matrix[:len(ordered_matrix) if len(ordered_matrix) < self.Knn_K else self.Knn_K])
            min_distance += mapped_matrix
        sorted_distance = sorted(min_distance, key=lambda x: x[1])
        print(sorted_distance)
        label_list = map(lambda x: x[0], sorted_distance[:len(sorted_distance) if len(sorted_distance) < self.Knn_K else self.Knn_K])
        return self.vote(label_list)

    def vote(self, label_list):
        if label_list is None or len(label_list) == 0:
            return None
        count_map = {}
        for clazz in label_list:
            count_map[clazz] = 1 if count_map.get(clazz) is None else count_map.get(clazz) + 1
        common = None
        times = 0
        for (k, v) in count_map.items():
            if v > times:
                common = k
                times = v
        return common

    def add_instance(self, record):
        points = self.models.get(record[-1])
        if points is None:
            points = []
            self.models[record[-1]] = points
        points.append(record[:-1])
        if len(points) > self.max_points_num:
            points = points[-self.max_points_num:]
            self.models[record[-1]] = points

    def stream_process(self, input_f, nums=None):
        for record in NumericSet(DataSet(input_f, nums), [41]):
            self.Time +=1
            self.reporter.preset(self.Time, record[-1])
            query = record[:-1]
            print("try to predict: {0}".format(record[-1]))
            # label = self.classify_using_mean_distance(query)
            # print("predict result using mean value: {0}".format(label))
            label = self.classify_using_min_distance(query)
            print("predict result using min value: {0}".format(label))
            if label is None:
                self.reporter.verify(self.Time, value = None, novel=True)
            else:
                self.reporter.verify(self.Time, value = label)
            self.add_instance(record)
            if self.Time % 2000 == 0:
                self.reporter.report()


if __name__ == "__main__":
    Alpha(100).stream_process("../data/kddcup.data_10_percent_corrected.minmax.shuffled", 2000)