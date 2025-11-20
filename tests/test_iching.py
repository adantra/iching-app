import unittest
from iching import IChing

class TestIChing(unittest.TestCase):
    def setUp(self):
        self.iching = IChing()

    def test_cast_coin(self):
        """Test that coin toss returns valid values (6, 7, 8, 9)."""
        for _ in range(100):
            val = self.iching.cast_coin()
            self.assertIn(val, [6, 7, 8, 9])

    def test_cast_hexagram_structure(self):
        """Test that hexagram generation returns correct structure."""
        result = self.iching.cast_hexagram()
        self.assertIn('raw_values', result)
        self.assertIn('hexagram', result)
        self.assertIn('future_hexagram', result)
        self.assertEqual(len(result['raw_values']), 6)
        self.assertEqual(len(result['hexagram']), 6)
        self.assertEqual(len(result['future_hexagram']), 6)

    def test_changing_lines(self):
        """Test logic for changing lines."""
        # Mock the cast_coin method to return specific values
        # 6 -> Old Yin (0) -> Becomes Yang (1)
        # 9 -> Old Yang (1) -> Becomes Yin (0)
        
        # We can't easily mock without a library or subclassing, 
        # so let's just check the logic consistency in the result
        result = self.iching.cast_hexagram()
        raw = result['raw_values']
        hex_lines = result['hexagram']
        fut_lines = result['future_hexagram']
        
        for i in range(6):
            val = raw[i]
            if val == 6:
                self.assertEqual(hex_lines[i], 0)
                self.assertEqual(fut_lines[i], 1)
            elif val == 9:
                self.assertEqual(hex_lines[i], 1)
                self.assertEqual(fut_lines[i], 0)
            elif val == 7:
                self.assertEqual(hex_lines[i], 1)
                self.assertEqual(fut_lines[i], 1)
            elif val == 8:
                self.assertEqual(hex_lines[i], 0)
                self.assertEqual(fut_lines[i], 0)

if __name__ == '__main__':
    unittest.main()
