# the algorithm proposed in
# "Classification and Novel Class Detection in Concept-Drifting Data Streams under Time Constraints"
#
# default parameters:
# number of pseudopoints, K=50
# minimum number of instances required to declare novel class, q = 50
# ensemble size, M = 6
# chunk size, S = 2000

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import numpy
from tools.dataset import DataSet, NumericSet, numeric_filter
from reporter import AccuracyBufferedReporter

class ECSMiner:

    def __init__(self):
        # init stage.
        # store: [[(weight, centroid, radius, mean distance, label), (...), ...], [...], [...]]
        self.models = []
        self.buf = []
        self.unlabeled = []
        self.labeled = []
        self.K = 50
        # instances # to start label novel class.
        self.q = 50
        # chunk size
        self.S = 2000
        # time starts from 0
        self.Time = 0
        # the k value of knn
        self.Knn_K = 1
        # time constraint to label
        self.Tl = 0
        # labeled records wait for enqueue
        self.label_buffer = []
        # ensemble size
        self.M = 6
        # last trait
        self.last_trait = 0
        # reporter
        self.reporter = AccuracyBufferedReporter()

    def stream_process(self, input_f, nums=None):
        # 41 here means we want to keep the class column
        for record in NumericSet(DataSet(input_f, nums), [41]):
            self.Time += 1
            # preset the actual label.
            self.reporter.preset(self.Time, record[-1])
            query = record[:-1]
            # classify
            self.classify(query)
            self.unlabeled.append(query)
            self.label_buffer.append(record)
            if len(self.unlabeled) > self.Tl:
                # print("giving label to : ", self.Time - self.Tl)
                self.labeled.append(self.label_buffer[0])
                self.label_buffer.remove(self.label_buffer[0])
                if len(self.labeled) == self.S:
                    # print("training a chunk, cluster num :" , self.K)
                    # train and
                    new_model = self.pseudopoints(self.labeled, self.K)
                    #print("new model: ", new_model)
                    # print("processed: ", self.Time)
                    self.reporter.report()
                    self.models.append(new_model)
                    if len(self.models) > self.M:
                        self.models = self.models[len(self.models) - self.M:]
                    self.labeled = []
        self.reporter.report()

    def pseudopoints(self, rawpoints, cluster_n):
        """
        generate pseudopoints using KMeans algorithm
        :param rawpoints: the raw points
        :return: generated pseudo points
        """
        # filter the categorical values
        numeric_list = map(lambda x : numeric_filter(x), rawpoints)
        mini_clusters = {}
        kmeans = KMeans(n_clusters = cluster_n).fit(numeric_list)
        for (index, label) in enumerate(kmeans.labels_):
            points = mini_clusters.get(label)
            if points is None:
                points = []
                mini_clusters[label] = points
            points.append(numeric_list[index] + rawpoints[index][-1:])
        # calculate pseudopoints
        pseudopoints = []
        for (label, items) in mini_clusters.items():
            weight = len(items)
            center = kmeans.cluster_centers_[label]
            total_distance = 0.0
            range_distance = 0.0
            label = {}
            for item in items:
                distance = euclidean_distances([center], [item[:-1]])[0][0]
                if distance > range_distance:
                    range_distance = distance
                total_distance += distance
                # append the label.
                count = label.get(item[-1])
                label[item[-1]] = 1 if count is None else count + 1
            # store: weight, center, range_distance, mean_distance.
            largest = 0
            final_label = None
            for k,v in label.items():
                if v > largest:
                    final_label = k
                    largest = v
            pseudopoints.append([weight, center, range_distance, total_distance / weight, final_label])
        return pseudopoints

    def classify(self, query):
        fout = True
        if not self.foutlier(query):
            label = self.majority_voting(query)
            # print("classify: ", label)
            self.reporter.verify(self.Time, label)
            fout = False
        self.filter_buffer()
        if fout:
            # print("regard as foutlier", len(self.buf), self.Time)
            self.buf.append([self.Time, query])
            if len(self.buf) > self.q and self.last_trait + self.q <= self.Time:
                self.last_trait = self.Time
                novel = self.detect_novel_class()
                if novel:
                    self.classify_and_remove_novel()

    def classify_and_remove_novel(self):
        for item in self.buf:
            self.reporter.verify(item[0], value = None, novel= True)
        self.reporter.watermark(self.buf[-1][0])
        self.buf = []

    def detect_novel_class(self):
        # print("detecting novel class:")
        cluster_num = self.K * len(self.buf) / self.S
        rawpoints = map(lambda x : x[1], self.buf)
        ppoints = self.pseudopoints(rawpoints, cluster_num)
        new_class_vote = 0
        for model in self.models:
            for index, ppoint in enumerate(ppoints):
                # compute q-NSC
                total_distance_between_foutlier = 0.0
                for index2, ppoint2 in enumerate(ppoints):
                    if index != index2:
                        this_distance = euclidean_distances([ppoint[1]], [ppoint2[1]])[0][0]
                        total_distance_between_foutlier += this_distance
                mean_distance_between_foutlier = total_distance_between_foutlier / len(ppoints) - 1
                minimum_distance_to_class = None
                for pcpoint in model:
                    this_distance = euclidean_distances([ppoint[1]], [pcpoint[1]])[0][0]
                    if minimum_distance_to_class is None or minimum_distance_to_class > this_distance:
                        minimum_distance_to_class = this_distance
                qNSC = (minimum_distance_to_class - mean_distance_between_foutlier) / \
                       max(minimum_distance_to_class, mean_distance_between_foutlier)
                if qNSC > 0 and ppoint[0] > self.q:
                    new_class_vote += 1
        # print("new class vote", new_class_vote)
        return True if new_class_vote == len(self.models) else False

    def foutlier(self, query):
        for model in self.models:
            for cluster in model:
                distance = euclidean_distances([query], [cluster[1]])[0][0]
                if distance <= cluster[2]:
                    return False
        return True

    def majority_voting(self, query):
        result = []
        for model in self.models:
            distances = []
            for pseudopoint in model:
                # calculate distance , store distance & label
                distances.append([euclidean_distances([pseudopoint[1]], [query])[0][0], pseudopoint[-1]])
            distances.sort(cmp = lambda x, y: cmp(x[0], y[0]))
            result.append(distances[0][1])
        return self.vote(result)

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

    def filter_buffer(self):
        # remove #1 scenario, according to the age.
        if len(self.buf) > 0:
            start_p = -1
            # while start_p +1 < len(self.buf) and self.buf[start_p + 1][0] < self.Time - self.S:
            #     start_p += 1
            # self.buf = self.buf[start_p:]
        #

if __name__ == '__main__':
    ECSMiner().stream_process("../data/kddcup.data_10_percent_corrected.minmax.shuffled", 100000)