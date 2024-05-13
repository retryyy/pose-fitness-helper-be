import unittest
from pose_analyze.pose_analyze_degree import _calculate_closed_degree_between_lines

class TestCalculateClosedDegreeBetweenLines(unittest.TestCase):
    def test_90_degree_angle(self):
        angle_deg = _calculate_closed_degree_between_lines((0, 0), (0, 1), (0, 0), (1, 0))
        self.assertAlmostEqual(angle_deg, 90, delta=0.01)

    def test_45_degree_angle(self):
        angle_deg = _calculate_closed_degree_between_lines((0, 0), (1, 1), (0, 0), (1, 0))
        self.assertAlmostEqual(angle_deg, 45, delta=0.01)

    def test_180_degree_angle(self):
        angle_deg = _calculate_closed_degree_between_lines((0, 0), (1, 0), (1, 0), (0, 0))
        self.assertAlmostEqual(angle_deg, 180, delta=0.01)

    def test_parallel_lines(self):
        angle_deg = _calculate_closed_degree_between_lines((0, 0), (0, 1), (1, 0), (1, 1))
        self.assertAlmostEqual(angle_deg, 0, delta=0.01)

if __name__ == '__main__':
    unittest.main()
