import sys
import numpy as np
from fastdtw import fastdtw
import numpy as np


def analyze_distance(all_points, benchmark_movement):
    arr1 = get_coordinates(all_points)
    arr2 = get_coordinates(benchmark_movement)

    np.set_printoptions(threshold=sys.maxsize)

    n1 = np.zeros_like(arr1)
    n2 = np.ones_like(arr2)

    res1, _ = fastdtw(n1, n2, dist=euclidean_distance)
    res2, _ = fastdtw(arr1, arr2, dist=euclidean_distance)

    return round(((res1 - res2) / res1) * 100)


def get_coordinates(points):
    array = np.array([[value for value in points[i].values()]
                     for i in range(len(points))])
    normalized_array = (array - np.min(array)) / \
        (np.max(array) - np.min(array))
    return normalized_array


def euclidean_distance(pose1, pose2):
    return np.linalg.norm(pose1 - pose2)
