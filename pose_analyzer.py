from enum import Enum
from pose_feedback import analyze_degree

from video_util import HEIGHT


RIGHT_ELBOW = 14
RIGHT_WRIST = 16

RIGHT_SHOULDER = 12
RIGHT_HIP = 24
RIGHT_KNEE = 26
RIGHT_ANKLE = 28

SIGMNA = 5


def pose_analyze(points, exercise_type, view):
    if exercise_type == 'SQUAT':
        if view == 'side':
            return squat_side(points)
        return {}

    return {}


def squat_side(points):
    checks = [{
        'func': lambda degree: degree > 170,
        'fulfilled': {
            'append': 'incorrect',
            'message': 'Too straight legs while standing which can hurt the knee with bigger weights',
        },
        'not_fulfilled': {
            'append': 'correct',
            'message': 'Knee is slightly bent which protects the joints'
        }
    }, {
        'func': lambda degree: degree < 95,
        'fulfilled': {
            'append': 'correct',
            'message': 'Went down enough for full muscle activation',
        },
        'not_fulfilled': {
            'append': 'incorrect',
            'message': "Didn't go down enough for full muscle activation"
        }
    }]

    return analyze_degree(points, (RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE), checks)
