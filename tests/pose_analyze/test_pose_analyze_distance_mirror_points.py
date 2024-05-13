import unittest
from pose_analyze.pose_analyze_distance import _mirror_points_x

class TestMirrorPointsX(unittest.TestCase):
    def test_mirror_points(self):
        points = [{"A": (1, 1), "B": (2, 3), "C": (4, 5)}]
        _mirror_points_x(points)
        self.assertDictEqual(
            points[0],
            {'A': [3, 1], 'B': [2, 3], 'C': [0, 5]}
        )

if __name__ == '__main__':
    unittest.main()
