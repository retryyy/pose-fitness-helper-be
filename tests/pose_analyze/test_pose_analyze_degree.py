import unittest
from pose_analyze.pose_analyze_degree import analyze_degree

class TestAnalyzeDegree(unittest.TestCase):
    frame_points = [{"A": (1, 1), "B": (0, 0), "C": (1, 0)}]

    def test_pose_analyze_degree_correct(self):
        checks = [{
            'func': lambda degree: degree < 50,
            'points': [("A", "B", "C")],
            'fulfilled': {
                'append': 'correct',
                'message': 'correct message',
            },
            'not_fulfilled': {
                'append': 'incorrect',
                'message': 'incorrect message'
            }
        }]
        
        result = analyze_degree(self.frame_points, checks)
        self.assertEqual(
            result,
            (['correct message'], [])
        )
    
    def test_pose_analyze_degree_incorrect(self):
        checks = [{
            'func': lambda degree: degree > 50,
            'points': [("A", "B", "C")],
            'fulfilled': {
                'append': 'correct',
                'message': 'correct message',
            },
            'not_fulfilled': {
                'append': 'incorrect',
                'message': 'incorrect message'
            }
        }]
        
        result = analyze_degree(self.frame_points, checks)
        self.assertEqual(
            result,
            ([], ['incorrect message'])
        )

if __name__ == '__main__':
    unittest.main()
