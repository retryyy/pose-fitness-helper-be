import numpy as np
from fastdtw import fastdtw
import numpy as np


def analyze_distance(all_points, benchmark_movement):
    res, _ = fastdtw(get_coordinates(all_points), get_coordinates(
        benchmark_movement), dist=euclidean_distance)
    print(res)
    return None


def get_coordinates(points):
    array = np.array([[value for value in points[i].values()]
                     for i in range(len(points))])
    normalized_array = (array - np.min(array)) / \
        (np.max(array) - np.min(array))
    return normalized_array


def euclidean_distance(pose1, pose2):
    return np.linalg.norm(pose1 - pose2)
