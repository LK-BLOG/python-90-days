# -*- coding: utf-8 -*-
import unittest

class TestDay03(unittest.TestCase):
    def test_closure(self):
        def make_multiplier(n):
            def m(x):
                return x * n
            return m
        double = make_multiplier(2)
        self.assertEqual(double(5), 10)

if __name__ == "__main__":
    unittest.main()
