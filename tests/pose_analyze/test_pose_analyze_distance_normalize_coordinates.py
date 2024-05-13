import unittest
import numpy as np
from pose_analyze.pose_analyze_distance import _normalize_coordinates

class TestNormalizeCoordinates(unittest.TestCase):
    def test_coordinates_normalization(self):
        points = [
            {
                "A": (2, 1),
                "B": (3, 3),
                "C": (4, 6)
            },
            {
                "A": (3, 4),
                "B": (2, 3),
                "C": (4, 5)
            }
        ]
        result = _normalize_coordinates(points)
        expected_result = np.array([
            [[0.0, 0.0], [0.5, 0.4], [1.0, 1.0]],
            [[0.5, 0.6], [0.0, 0.4], [1.0, 0.8]]
        ])
        np.testing.assert_array_almost_equal(result, expected_result, decimal=2)
    
    def test_coordinates_normalization_min_max_equals(self):
        points = [{
            "A": [2, 1],
            "B": [2, 3],
            "C": [2, 6]
        }]
        with self.assertRaises(Exception) as context:
            _normalize_coordinates(points)
        
        self.assertTrue("Input data is a line!", str(context.exception))


if __name__ == '__main__':
    unittest.main()
