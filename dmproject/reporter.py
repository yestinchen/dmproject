
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
