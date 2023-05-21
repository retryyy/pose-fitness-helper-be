from pose import POSE_DEGREE_CHECK
from pose_feedback import analyze_degree


def pose_analyze(points, exercise_type, view):
    return analyze_degree(points, POSE_DEGREE_CHECK[exercise_type][view])
