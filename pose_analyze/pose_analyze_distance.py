import numpy as np
from fastdtw import fastdtw
import copy


def analyze_correlation_by_distance(all_points, benchmark_movement):
    res1 = _correlation(all_points, benchmark_movement)
    res2 = _correlation(all_points, benchmark_movement, True)
    return max(res1, res2)


def _correlation(all_points, benchmark_movement, mirror=False):
    all_points_copy = copy.deepcopy(all_points)
    benchmark_movement_copy = copy.deepcopy(benchmark_movement)
    if mirror:
        _mirror_points_x(all_points_copy)

    arr1 = _normalize_coordinates(all_points_copy)
    arr2 = _normalize_coordinates(benchmark_movement_copy)

    n1 = np.zeros_like(arr1)
    n2 = np.ones_like(arr2)

    res1, _ = fastdtw(n1, n2, dist=_euclidean_distance)
    res1 /= 2
    res2, _ = fastdtw(arr1, arr2, dist=_euclidean_distance)

    return round(((res1 - res2) / res1) * 100)


def _normalize_coordinates(points):
    array = np.array([
        [value for value in points[i].values()] for i in range(len(points))
    ])
    x_coords = array[:, :, 0]
    y_coords = array[:, :, 1]

    x_min = np.min(x_coords)
    x_max = np.max(x_coords)
    y_min = np.min(y_coords)
    y_max = np.max(y_coords)

    x_diff = x_max - x_min
    y_diff = y_max - y_min

    if x_diff == 0 or y_diff == 0:
        raise Exception("Input data is a line!")

    normalized_x_coords = (x_coords - x_min) / x_diff
    normalized_y_coords = (y_coords - y_min) / y_diff

    normalized_array = np.dstack((normalized_x_coords, normalized_y_coords))
    return normalized_array


def _euclidean_distance(pose1, pose2):
    return np.linalg.norm(pose1 - pose2)


def _mirror_points_x(points):
    max_x = 0
    for point in points:
        for x, _ in point.values():
            max_x = x if max_x < x else max_x

    for point in points:
        for k in point.keys():
            x, y = point[k]
            point[k] = [max_x - x, y]
