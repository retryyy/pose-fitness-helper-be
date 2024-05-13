import unittest
from pose_analyze.pose_analyze_distance import _correlation

class TestCorrelation(unittest.TestCase):
    test_points_1 = [{
        "A": (2, 1),
        "B": (3, 3),
        "C": (4, 6)
    }]
    test_points_2 = [{
        "A": (2, 1),
        "B": (3, 3),
        "C": (4, 7)
    }]

    def test_correlation_100(self):
        result = _correlation(self.test_points_1, self.test_points_1)
        self.assertEqual(100, result)
    
    def test_correlation_95(self):
        result = _correlation(self.test_points_1, self.test_points_2)
        self.assertEqual(95, result)

if __name__ == '__main__':
    unittest.main()
