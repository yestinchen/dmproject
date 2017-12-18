# simple knn
import utilities
from tools.dataset import DataSet
from reporter import AccuracyReporter


class KnnProcessor:

    def __init__(self, training_size = None):
        self.training_set = []
        self.training_size = training_size


    def search_top_k(self, query, k):
        """
        search the top k classifications for item
        :param query: the input vector
        :param k: the number of nearest neighbor
        :return: the classification result order by distance.[(distance, result_k)]
        """
        result = []
        for item in self.training_set:
            d = utilities.calculate_distance(query, item[:-1])
            result.append((d, item))
            if len(result) > k:
                # replace
                result.sort(key = lambda (x,y) : x)
                result = result[:-1]
        return result

    def get_most_frequent_label(self, top_k_result):
        """
        get the most frequent label from top_k_result.
        :param top_k_result:
        :return:
        """
        if top_k_result is None or len(top_k_result) == 0:
            return None
        count_map = {}
        for (distance, item) in top_k_result:
            clazz = item[-1]
            count_map[clazz] = 1 if count_map.get(clazz) is None else count_map.get(clazz) + 1
        common = None
        times = 0
        for (k, v) in count_map.items():
            if v > times:
                common = k
                times = v
        return common

    def stream_process(self, input_name, lines = None, k = 1):
        reporter = AccuracyReporter()
        for index, item in enumerate(DataSet(input_name, lines)):
            label = self.get_most_frequent_label(self.search_top_k(item[:-1], k))
            self.training_set.append(item)
            if self.training_size is not None and len(self.training_set) > self.training_size:
                self.training_set.remove(self.training_set[0])
            reporter.track(index, item[-1], label)
        reporter.report()


if __name__ == '__main__':
    # print(get_most_frequent_label([(1,'a'), (2, 'b'), (3, 'c'), (3, 'c')]))
    knnProcessor = KnnProcessor(10)
    knnProcessor.stream_process("../data/kddcup.data_10_percent_corrected.minmax.shuffled")
