# -*- coding: utf-8 -*-
import unittest

class TestDay02(unittest.TestCase):
    def test_lambda(self):
        square = lambda x: x ** 2
        self.assertEqual(square(5), 25)

    def test_map_filter(self):
        numbers = [1, 2, 3, 4, 5]
        self.assertEqual(list(map(lambda x: x * 2, numbers)), [2, 4, 6, 8, 10])

if __name__ == "__main__":
    unittest.main()
