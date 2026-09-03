# -*- coding: utf-8 -*-
import unittest
class TestDay06(unittest.TestCase):
    def test_safe_divide(self):
        def safe_divide(a, b):
            try:
                return a / b
            except ZeroDivisionError:
                return None
        self.assertAlmostEqual(safe_divide(10, 3), 3.333, places=2)
        self.assertIsNone(safe_divide(10, 0))
if __name__ == "__main__":
    unittest.main()
