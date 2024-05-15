LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_HIP = 23
RIGHT_HIP = 24
RIGHT_KNEE = 26
RIGHT_ANKLE = 28

POSE_DEGREE_CHECK = {
    'DUMBBELL_SQUAT': {
        'side': [
            {
                'func': lambda degree: degree < 95,
                'points': [(RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE)],
                'fulfilled': {
                    'append': 'correct',
                    'message': 'Went down enough for full muscle activation',
                },
                'not_fulfilled': {
                    'append': 'incorrect',
                    'message': "Didn't go down enough for full muscle activation"
                }
            }, {
                'func': lambda degree: degree < 90,
                'points': [(RIGHT_ANKLE, RIGHT_HIP, RIGHT_SHOULDER)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Bent over too much, pushed from back and not from leg',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': 'Perfectly held back (not bent over much), pushed weight from leg'
                }
            }, {
                'func': lambda degree: degree > 170,
                'points': [(RIGHT_SHOULDER, RIGHT_WRIST, RIGHT_ANKLE)],
                'fulfilled': {
                    'append': 'correct',
                    'message': 'Kept hands next to the body for full balance',
                },
                'not_fulfilled': {
                    'append': 'incorrect',
                    'message': "Didn\'t keep hands next to the body for full balance"
                }
            }, {
                'func': lambda degree: degree < 150,
                'points': [(RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Didn\'t keep hands totally straight',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': "Kept hands totally straight"
                }
            }
        ]
    },
    'BARBELL_BACK_SQUAT': {
        'front': [
            {
                'func': lambda degree: degree > 90,
                'points': [(RIGHT_SHOULDER, RIGHT_KNEE, LEFT_HIP)],
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
                'points': [(RIGHT_SHOULDER, LEFT_SHOULDER, RIGHT_HIP, LEFT_HIP)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Either the shoulders or the wrists were not horizontal',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': "Perfectly held the shoulders and the wrists horizontally"
                }
            }
        ]
    },
    'SHOULDER_PRESS': {
        'front': [
            {
                'func': lambda degree: degree < 100,
                'points': [(RIGHT_WRIST, RIGHT_SHOULDER, LEFT_SHOULDER)],
                'fulfilled': {
                    'append': 'correct',
                    'message': 'Contracted hands on top enough',
                },
                'not_fulfilled': {
                    'append': 'incorrect',
                    'message': 'Hands were pointing too much outwards on the top'
                }
            }, {
                'func': lambda degree: degree < 60,
                'points': [(RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_HIP)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Lowered hands too much which can cause shoulder pain',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': "Didn't let the elbows too much under the shoulders"
                }
            }, {
                'func': lambda degree: degree > 5,
                'points': [(RIGHT_SHOULDER, LEFT_SHOULDER, RIGHT_WRIST, LEFT_WRIST)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Either the shoulders or the wrists were not horizontal',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': "Perfectly held the shoulders and the wrists horizontally"
                }
            }
        ]
    },
    'DUMBBELL_LATERAL_RAISE': {
        'side': [
            {
                'func': lambda degree: degree > 160,
                'points': [(RIGHT_KNEE, RIGHT_HIP, RIGHT_SHOULDER)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Standing too straight, should bend a little',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': 'Legs were not too straight'
                }
            }, {
                'func': lambda degree: degree < 20,
                'points': [(RIGHT_WRIST, RIGHT_SHOULDER, RIGHT_HIP)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Should raise the dumbbel slightly forward',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': "Raised the dumbbel slightly forward"
                }
            }
        ]
    },
    'DUMBBELL_ROMANIAN_DEADLIFT': {
        'side': [
            {
                'func': lambda degree: degree < 90,
                'points': [(RIGHT_SHOULDER, RIGHT_HIP, RIGHT_ANKLE)],
                'fulfilled': {
                    'append': 'correct',
                    'message': 'Went down enough for full hamstring stretch',
                },
                'not_fulfilled': {
                    'append': 'incorrect',
                    'message': 'Didn\'t go down enough for full hamstring stretch'
                }
            },
            {
                'func': lambda degree: degree < 150,
                'points': [(RIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Legs were not straight enough for full hamstring stretch',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': 'Legs were straight enough for full hamstring stretch'
                }
            }
        ]
    },
    'CLOSE_GRIP_CABLE_ROW': {
        'side': [
            {
                'func': lambda degree: degree > 120,
                'points': [(RIGHT_SHOULDER, RIGHT_HIP, RIGHT_KNEE)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Leaned back too much, arms are taking over the stress from the back',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': 'Didn\'t lean back too much, primary back muscles were used'
                }
            },
            {
                'func': lambda degree: degree < 90,
                'points': [
                    (RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST),
                    (LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
                ],
                'fulfilled': {
                    'append': 'correct',
                    'message': 'Pulled weight back enough for proper form',
                },
                'not_fulfilled': {
                    'append': 'incorrect',
                    'message': 'Didn\'t pull weight back enough to contract back muscles'
                }
            }
        ]
    },
    'TRICEPS_PUSHDOWN': {
        'side': [
            {
                'func': lambda degree: degree > 30,
                'points': [(RIGHT_HIP, RIGHT_SHOULDER, RIGHT_ELBOW)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Too much shoulder movement',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': 'Didn\'t move shoulder too much'
                }
            },
            {
                'func': lambda degree: degree > 160,
                'points': [(RIGHT_SHOULDER, RIGHT_HIP, RIGHT_KNEE)],
                'fulfilled': {
                    'append': 'incorrect',
                    'message': 'Standing too straight, should bend a little',
                },
                'not_fulfilled': {
                    'append': 'correct',
                    'message': 'Legs were not too straight'
                }
            },
            {
                'func': lambda degree: degree < 90,
                'points': [(RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)],
                'fulfilled': {
                    'append': 'correct',
                    'message': 'Bent the elbow enough for full triceps stretch',
                },
                'not_fulfilled': {
                    'append': 'incorrect',
                    'message': 'Didn\'t bend the elbow enough for full triceps stretch'
                }
            },
        ]
    },
}
