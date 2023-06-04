import numpy as np
from fastdtw import fastdtw
import copy


def analyze_distance(all_points, benchmark_movement):
    res1 = distance(all_points, benchmark_movement)
    res2 = distance(all_points, benchmark_movement, True)
    return max(res1, res2)


def distance(all_points, benchmark_movement, mirror=False):
    all_points_copy = copy.deepcopy(all_points)
    benchmark_movement_copy = copy.deepcopy(benchmark_movement)
    if mirror:
        mirror_points_x(all_points_copy)
    normalize_points(all_points_copy)
    normalize_points(benchmark_movement_copy)

    arr1 = get_coordinates(all_points_copy)
    arr2 = get_coordinates(benchmark_movement_copy)

    n1 = np.zeros_like(arr1)
    n2 = np.ones_like(arr2)

    res1, _ = fastdtw(n1, n2, dist=euclidean_distance)
    res1 /= 2
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


def normalize_points(points):
    min_x, min_y = 1000, 1000
    for point in points:
        for x, y in point.values():
            min_x = x if x < min_x else min_x
            min_y = y if y < min_y else min_y

    for point in points:
        for k in point.keys():
            x, y = point[k]
            point[k] = [x - min_x, y - min_y]


def mirror_points_x(points):
    max_x = 0
    for point in points:
        for x, _ in point.values():
            max_x = x if max_x < x else max_x

    for point in points:
        for k in point.keys():
            x, y = point[k]
            point[k] = [max_x - x, y]
