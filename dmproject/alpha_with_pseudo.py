# solution a

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import numpy
from tools.dataset import DataSet, NumericSet, numeric_filter
from reporter import AccuracyBufferedReporter


class PseudoPoint:
    def __init__(self, weight, centroid, mean_distance, radius):
        self.weight = weight
        self.centroid = centroid
        self.mean_distance = mean_distance
        self.radius = radius

class Alpha:
    """
    plan a
    """

    def __init__(self, max_points_num = 10):
        self.Time = 0
        self.reporter = AccuracyBufferedReporter()
        # label, model
        self.models = {}
        self.max_points_num = max_points_num

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
        min_distance = {}
        for label, points in self.models.items():
            distance_matrix = euclidean_distances([query], points)
            md = None
            for d in distance_matrix[0]:
                if md is None or md > d:
                    md = d
            min_distance[label] = md
        sorted_distance = sorted(min_distance.items(), key=lambda x: x[1])
        # print(sorted_distance)
        return None if len(sorted_distance) == 0 else sorted_distance[0][0]

    def add_instance(self, record):
        points = self.models.get(record[-1])
        if points is None:
            points = []
            self.models[record[-1]] = points
        if len(points) + 1 <= self.max_points_num:
            pseudop = PseudoPoint(1, record, 0.0, 0.0)
            points.append(pseudop)
        else:
            # find a merger.
            all_centroids = map(lambda x : x.cetroid, points)
            all_radius = map(lambda x: x.raduis, points)

        points.append(record[:-1])
        if len(points) > self.max_points_num:
            points = points[-self.max_points_num:]
            self.models[record[-1]] = points

    def stream_process(self, input_f, nums=None):
        for record in NumericSet(DataSet(input_f, nums), [41]):
            self.Time +=1
            self.reporter.preset(self.Time, record[-1])
            query = record[:-1]
            # print("try to predict: {0}".format(record[-1]))
            label = self.classify_using_min_distance(query)
            # print("predict result: {0}".format(label))
            if label is None:
                self.reporter.verify(self.Time, value = None, novel=True)
            else:
                self.reporter.verify(self.Time, value = label)
            self.add_instance(record)
            if self.Time % 2000 == 0:
                self.reporter.report()

if __name__ == "__main__":
    Alpha(100).stream_process("../data/kddcup.data_10_percent_corrected.minmax.shuffled", 100000)