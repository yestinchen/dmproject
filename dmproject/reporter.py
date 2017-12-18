
class AccuracyReporter:
    """
    Track on accuracy
    """

    def __init__(self):
        self.accurate_count = 0
        self.inaccurate_count = 0
        self.history = []

    def track(self, id, expected, actual):
        #print("id:{0}, expected: {1}, actual: {2}".format(id, expected, actual))
        if expected == actual:
            self.accurate_count += 1
            self.history.append((id, True))
        else:
            self.inaccurate_count += 1
            self.history.append((id, False))


    def report(self, output_file = None):
        if output_file is None:
            print("accuracy: {0}, total: {1}".format(float(self.accurate_count) / (self.accurate_count + self.inaccurate_count),
                                         self.accurate_count + self.inaccurate_count))
            print("accurate count: {0}, inaccurate: {1}".format(self.accurate_count, self.inaccurate_count))
        else:
            pass

class AccuracyBufferedReporter:

    def __init__(self):
        self.accurate_count = 0
        self.inaccurate_count = 0
        self.history = []
        self.actual_buffer = {}
        self.classify_buffer = {}
        self.all_labels_so_far = []
        self.last_watermark = 0

    def preset(self, id, value):
        """
        preset the actual label for the item
        :param id:
        :param value:
        :return:
        """
        self.actual_buffer[id] = value

    def watermark(self, watermark):
        for i in [self.last_watermark, watermark]:
            if self.actual_buffer[i] not in self.all_labels_so_far:
                self.all_labels_so_far.append(self.actual_buffer[i])

    def verify(self, id, value = None, novel=False):
        self.classify_buffer[id] = value
        if value == self.actual_buffer[id]:
            self.accurate_count += 1
        elif novel and self.classify_buffer[id] not in self.all_labels_so_far:
            self.accurate_count += 1
        else:
            print("should be : {0}, but classified as: {1}, novel = {2}".format(
                self.actual_buffer[id], value, novel))

    def report(self, output_file = None):
        if output_file is None:
            print("accuracy:{0}, total: {1}".format(
                float(self.accurate_count) / len(self.actual_buffer), len(self.actual_buffer)))