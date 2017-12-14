import math


def calculate_distance(a, b):
    """
    calculate distance between two vectors.
    :param a:
    :param b:
    :return: the distance
    """
    distance = 0.0
    for (index, va) in enumerate(a):
        vb = b[index]
        if va is float or va is int:
            distance += math.pow(va - vb, 2)
        else:
            distance += (0 if va == vb else 1)
    return 0 if distance == 0 else math.sqrt(distance)


if __name__ == "__main__":
    print(calculate_distance([1, 2], [1, 2]))
    print(calculate_distance([1, 'a'], [1, 'a']))
    print(calculate_distance([1, 'a'], [1, 'b']))
    print(calculate_distance([1, 'a'], [3, 'b']))