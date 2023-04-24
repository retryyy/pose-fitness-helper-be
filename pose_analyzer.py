from pose_feedback import analyze_degree

LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_HIP = 23
RIGHT_HIP = 24
RIGHT_KNEE = 26
RIGHT_ANKLE = 28


def pose_analyze(points, exercise_type, view):
    if exercise_type == 'SQUAT':
        if view == 'side':
            return squat_side(points)
        elif view == 'front':
            return squat_front(points)
        return {}
    elif exercise_type == 'DUMBBELL_SHOULDER_PRESS':
        if view == 'front':
            return dumbbell_shoulder_press_front(points)

    return {}


def squat_side(points):
    checks = [{
        'func': lambda degree: degree > 170,
        'points': (RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE),
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
        'points': (RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE),
        'fulfilled': {
            'append': 'correct',
            'message': 'Went down enough for full muscle activation',
        },
        'not_fulfilled': {
            'append': 'incorrect',
            'message': "Didn't go down enough for full muscle activation"
        }
    }]

    return analyze_degree(points, checks)

def squat_front(points):
    checks = [{
        'func': lambda degree: degree > 90,
        'points': (RIGHT_SHOULDER, RIGHT_KNEE, LEFT_HIP),
        'fulfilled': {
            'append': 'incorrect',
            'message': 'Knees are pointing inside too much that can cause knee pain',
        },
        'not_fulfilled': {
            'append': 'correct',
            'message': 'Knees are pointing outside which is good for the knees'
        }
    }, {
        'func': lambda degree: degree > 5,
        'points': (RIGHT_SHOULDER, LEFT_SHOULDER, RIGHT_HIP, LEFT_HIP),
        'fulfilled': {
            'append': 'incorrect',
            'message': 'Either the shoulders or the wrists are not horizontal',
        },
        'not_fulfilled': {
            'append': 'correct',
            'message': "Perfectly held the shoulders and the wrists horizontally"
        }
    }]

    return analyze_degree(points, checks)

def dumbbell_shoulder_press_front(points):
    checks = [{
        'func': lambda degree: degree < 100,
        'points': (RIGHT_WRIST, RIGHT_SHOULDER, LEFT_SHOULDER),
        'fulfilled': {
            'append': 'correct',
            'message': 'Contracted hands on top enough',
        },
        'not_fulfilled': {
            'append': 'incorrect',
            'message': 'Hands are pointing too much to the sides on the top'
        }
    }, {
        'func': lambda degree: degree < 70,
        'points': (RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_HIP),
        'fulfilled': {
            'append': 'incorrect',
            'message': 'Lowering hands too much can cause shoulder pain',
        },
        'not_fulfilled': {
            'append': 'correct',
            'message': "Didn't let elbows too under the shoulder"
        }
    }, {
        'func': lambda degree: degree > 5,
        'points': (RIGHT_SHOULDER, LEFT_SHOULDER, RIGHT_WRIST, LEFT_WRIST),
        'fulfilled': {
            'append': 'incorrect',
            'message': 'Either the shoulders or the wrists are not horizontal',
        },
        'not_fulfilled': {
            'append': 'correct',
            'message': "Perfectly held the shoulders and the wrists horizontally"
        }
    }]

    return analyze_degree(points, checks)
