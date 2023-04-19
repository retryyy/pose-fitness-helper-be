import math


def analyze_degree(all_points, analyze_points, checks):
    (point1, point2, point3) = analyze_points

    for check in checks:
        check['truth'] = False

    correct = []
    incorrect = []

    for point_object in all_points:
        degree = calculate_degree(
            point_object, point1, point2, point3)

        for check in checks:
            if not check['truth']:
                res = check['func'](degree)
                if res:
                    check['truth'] = True

    for check in checks:
        elem = check['fulfilled' if check['truth'] else 'not_fulfilled']
        message = elem['message']

        if elem['append'] == "correct":
            correct.append(message)
        else:
            incorrect.append(message)

    return collect_result(correct, incorrect, 80)


def collect_result(correct, incorrect, score):
    return {
        'correct': correct,
        'incorrect': incorrect,
        'score': score
    }


def calculate_degree(points, point_name1, point_name2, point_name3):
    x1, y1 = points[str(point_name1)]
    x2, y2 = points[str(point_name2)]
    x3, y3 = points[str(point_name3)]

    return calculate_closed_degree(x1, y1, x2, y2, x3, y3)


def calculate_closed_degree(x1, y1, x2, y2, x3, y3):
    dx1 = x1 - x2
    dy1 = y1 - y2
    dx2 = x3 - x2
    dy2 = y3 - y2

    dot_product = dx1*dx2 + dy1*dy2
    magnitude1 = math.sqrt(dx1**2 + dy1**2)
    magnitude2 = math.sqrt(dx2**2 + dy2**2)
    angle_rad = math.acos(dot_product / (magnitude1 * magnitude2))

    angle_deg1 = math.degrees(angle_rad)

    return angle_deg1
