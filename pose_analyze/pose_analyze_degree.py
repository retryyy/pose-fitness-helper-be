import math


def analyze_degree(all_points, checks):
    for check in checks:
        check['truth'] = False

    correct = []
    incorrect = []

    for point_object in all_points:
        for check in checks:
            point_checks = check['points']

            for points in point_checks:
                if len(points) == 3:
                    (point1, point2, point3) = points
                    degree = _calculate_closed_degree(
                        point_object[str(point1)],
                        point_object[str(point2)],
                        point_object[str(point3)]
                    )
                elif len(points) == 4:
                    (point1, point2, point3, point4) = points
                    degree = _calculate_closed_degree_between_lines(
                        point_object[str(point1)],
                        point_object[str(point2)],
                        point_object[str(point3)],
                        point_object[str(point4)]
                    )

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

    return correct, incorrect

def _calculate_closed_degree(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    dx1 = x1 - x2
    dy1 = y1 - y2
    dx2 = x3 - x2
    dy2 = y3 - y2

    dot_product = dx1*dx2 + dy1*dy2
    magnitude1 = math.sqrt(dx1**2 + dy1**2)
    magnitude2 = math.sqrt(dx2**2 + dy2**2)

    calc = _get_calc(dot_product / (magnitude1 * magnitude2))
    angle_rad = math.acos(calc)

    angle_deg = math.degrees(angle_rad)
    return angle_deg


def _calculate_closed_degree_between_lines(point1, point2, point3, point4):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x4, y4 = point4

    line1_start = (x1, y1)
    line1_end = (x2, y2)
    line2_start = (x3, y3)
    line2_end = (x4, y4)

    line1_dx = line1_end[0] - line1_start[0]
    line1_dy = line1_end[1] - line1_start[1]
    line2_dx = line2_end[0] - line2_start[0]
    line2_dy = line2_end[1] - line2_start[1]

    dot_product = line1_dx*line2_dx + line1_dy*line2_dy
    magnitude1 = math.sqrt(line1_dx**2 + line1_dy**2)
    magnitude2 = math.sqrt(line2_dx**2 + line2_dy**2)
    calc = _get_calc(dot_product / (magnitude1 * magnitude2))
    angle_rad = math.acos(calc)

    angle_deg = math.degrees(angle_rad)

    return angle_deg


def _get_calc(num):
    if num > 1:
        return 1
    elif num < 0:
        return 0
    else:
        return num
