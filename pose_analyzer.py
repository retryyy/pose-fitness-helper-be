import json
from pose import POSE_DEGREE_CHECK
from pose_analyze_degree import analyze_degree
from pose_analyze_distance import analyze_distance


def pose_analyze(points, exercise_type, view):
    with open(f"./benchmark_exercises/{exercise_type}-{view}.json", "r") as read_file:
        benchmark_points = json.load(read_file)['points']
        result_distance = analyze_distance(points, benchmark_points)
    
    return analyze_degree(points, POSE_DEGREE_CHECK[exercise_type][view])
