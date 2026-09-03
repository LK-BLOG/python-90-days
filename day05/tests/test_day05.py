# -*- coding: utf-8 -*-
import unittest
class TestDay05(unittest.TestCase):
    def test_comprehension(self):
        result = [x**2 for x in range(5)]
        self.assertEqual(result, [0, 1, 4, 9, 16])
    def test_counter(self):
        from collections import Counter
        c = Counter("aab")
        self.assertEqual(c['a'], 2)
if __name__ == "__main__":
    unittest.main()
