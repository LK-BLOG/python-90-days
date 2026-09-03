# -*- coding: utf-8 -*-
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter'))
class TestBuildMessages(unittest.TestCase):
    def test_basic(self):
        from importlib import import_module
        m = import_module("01_basic_practice")
        r = m.build_messages("sys","usr")
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]["role"], "system")
    def test_cost(self):
        from importlib import import_module
        m = import_module("01_basic_practice")
        c = m.calc_cost(1_000_000, 1_000_000)
        self.assertAlmostEqual(c, 0.75, places=4)
if __name__ == "__main__":
    unittest.main()
