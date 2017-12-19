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

    def __init__(self, max_points_num = 10, knn_k = 1, cluster_n = 50):
        self.Time = 0
        self.reporter = AccuracyBufferedReporter()
        # label, model
        self.models = []
        self.buffer = []
        self.max_points_num = max_points_num
        self.Knn_K = knn_k
        self.cluster_n = cluster_n

    def classify_using_min_distance(self, query):
        if len(self.models) == 0:
            return None
        min_distance = []
        for model in self.models:
            for label, points in model.items():
                distance_matrix = euclidean_distances([query], map(lambda x: x[1], points))
                ordered_matrix = sorted(distance_matrix[0])
                mapped_matrix = map(lambda x: [label, x],
                                ordered_matrix[:len(ordered_matrix) if len(ordered_matrix) < self.Knn_K else self.Knn_K])
                min_distance += mapped_matrix
        sorted_distance = sorted(min_distance, key=lambda x: x[1])
        # print(sorted_distance)
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
        self.buffer.append(record)
        if len(self.buffer) > 1000:
            grouped_clusters = {}
            # split the buffer into different groups
            grouped_buffer = {}
            for r in self.buffer:
                points = grouped_buffer.get(r[-1])
                if points is None:
                    points = []
                    grouped_buffer[r[-1]] = points
                points.append(r[:-1])
            # handle grouped buffer
            for label, points in grouped_buffer.items():
                pseudopoints = []
                if len(points) >= self.cluster_n:
                    mini_clusters = {}
                    kmeans = KMeans(n_clusters= self.cluster_n).fit(points)
                    for (index, l) in enumerate(kmeans.labels_):
                        ps = mini_clusters.get(l)
                        if ps is None:
                            ps = []
                            mini_clusters[l] = ps
                        ps.append(points[index])
                    for (l, items) in mini_clusters.items():
                        weight = len(items)
                        center = kmeans.cluster_centers_[l]
                        total_distance = 0.0
                        range_distance = 0.0
                        for item in items:
                            distance = euclidean_distances([center], [item])[0][0]
                            if distance > range_distance:
                                range_distance = distance
                            total_distance += distance
                        # store: weight, center, range_distance, mean_distance.
                        pseudopoints.append([weight, center, range_distance, total_distance / weight])
                else:
                    for p in points:
                        pseudopoints.append([1, p, 0, 0])
                grouped_clusters[label] = pseudopoints
            self.models.append(grouped_clusters)
            self.buffer=[]
            if len(self.models) > 5:
                self.models = self.models[-5:]

    def stream_process(self, input_f, nums=None):
        for record in NumericSet(DataSet(input_f, nums), [41]):
            self.Time +=1
            self.reporter.preset(self.Time, record[-1])
            query = record[:-1]
            #print("try to predict: {0}".format(record[-1]))
            # label = self.classify_using_mean_distance(query)
            # print("predict result using mean value: {0}".format(label))
            label = self.classify_using_min_distance(query)
            #print("predict result using min value: {0}".format(label))
            if label is None:
                self.reporter.verify(self.Time, value = None, novel=True)
            else:
                self.reporter.verify(self.Time, value = label)
            self.add_instance(record)
            if self.Time % 2000 == 0:
                self.reporter.report()


if __name__ == "__main__":
    Alpha(100).stream_process("../data/kddcup.data_10_percent_corrected.minmax.shuffled", 100000)