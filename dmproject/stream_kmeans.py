# Simply implement a stream kmeans algorithm

import random


class CoresetTreeElem:
    def __init__(self, n, points, center):
        self.n = n
        self.points = points
        self.center = center

class CoresetTreeLeaf:
    def __init__(self, elements, cost):
        self.elements = elements
        self.cost = cost

    def costOfPoint(self, point):
        weight = point[0]
        instance = point



class TreeCoreset:

    def __init__(self, m, points):
        init_center = points[random.randrange(0, len(points))]


class StreamKmeans:

    def __init__(self):
        pass

