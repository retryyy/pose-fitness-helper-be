import json
from pose import POSE_DEGREE_CHECK
from pose_analyze_degree import analyze_degree
from pose_analyze_distance import analyze_distance


def pose_analyze(points, exercise_type, view):
    with open(f"./benchmark_exercises/{exercise_type}-{view}.json", "r") as read_file:
        points_to_check = list(points[0].keys())
        reduced_benchmark_points = reduce_points(
            json.load(read_file)['points'], 
            points_to_check
        )
        result_distance = analyze_distance(points, reduced_benchmark_points)

    checks = POSE_DEGREE_CHECK.get(exercise_type, {}).get(view)
    if checks is not None:
        result_degree_correct, result_degree_incorrect = analyze_degree(
            points, POSE_DEGREE_CHECK[exercise_type][view])
    else:
        result_degree_correct, result_degree_incorrect = [], []

    return collect_result(result_degree_correct,
                          result_degree_incorrect,
                          result_distance)

def reduce_points(base_points, points_to_check):
    return [
        {i: frame[i] for i in frame if i in points_to_check}
        for frame in base_points
    ]

def collect_result(correct, incorrect, score):
    return {
        'correct': correct,
        'incorrect': incorrect,
        'score': score
    }
