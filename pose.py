LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_HIP = 23
RIGHT_HIP = 24
RIGHT_KNEE = 26
RIGHT_ANKLE = 28

POSE_DEGREE_CHECK = {
    'BARBELL_BACK_SQUAT': {
        'side': [{
            'func': lambda degree: degree > 170,
            'points': (RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE),
            'fulfilled': {
                'append': 'incorrect',
                'message': 'Legs were too straight while standing which can hurt the knee using bigger weights',
            },
            'not_fulfilled': {
                'append': 'correct',
                'message': 'Knees were slightly bent which protects the joints'
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
        }],
        'front': [{
            'func': lambda degree: degree > 90,
            'points': (RIGHT_SHOULDER, RIGHT_KNEE, LEFT_HIP),
            'fulfilled': {
                'append': 'incorrect',
                'message': 'Knees were pointing inwards too much that can cause knee pain',
            },
            'not_fulfilled': {
                'append': 'correct',
                'message': 'Knees were pointing outwards which is good for the knees'
            }
        }, {
            'func': lambda degree: degree > 10,
            'points': (RIGHT_SHOULDER, LEFT_SHOULDER, RIGHT_HIP, LEFT_HIP),
            'fulfilled': {
                'append': 'incorrect',
                'message': 'Either the shoulders or the wrists were not horizontal',
            },
            'not_fulfilled': {
                'append': 'correct',
                'message': "Perfectly held the shoulders and the wrists horizontally"
            }
        }]
    },
    'DUMBBELL_SHOULDER_PRESS': {
        'front': [{
            'func': lambda degree: degree < 100,
            'points': (RIGHT_WRIST, RIGHT_SHOULDER, LEFT_SHOULDER),
            'fulfilled': {
                'append': 'correct',
                'message': 'Contracted hands on top enough',
            },
            'not_fulfilled': {
                'append': 'incorrect',
                'message': 'Hands were pointing too much outwards on the top'
            }
        }, {
            'func': lambda degree: degree < 70,
            'points': (RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_HIP),
            'fulfilled': {
                'append': 'incorrect',
                'message': 'Lowered hands too much which can cause shoulder pain',
            },
            'not_fulfilled': {
                'append': 'correct',
                'message': "Didn't let elbows too much under the shoulders"
            }
        }, {
            'func': lambda degree: degree > 5,
            'points': (RIGHT_SHOULDER, LEFT_SHOULDER, RIGHT_WRIST, LEFT_WRIST),
            'fulfilled': {
                'append': 'incorrect',
                'message': 'Either the shoulders or the wrists were not horizontal',
            },
            'not_fulfilled': {
                'append': 'correct',
                'message': "Perfectly held the shoulders and the wrists horizontally"
            }
        }]
    }
}
