# -*- coding: utf-8 -*-
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter'))

class TestDay70(unittest.TestCase):
    def test_import(self):
        """确保starter模块可以导入"""
        import importlib
        files = [f for f in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'starter')) if f.endswith('.py') and f != '__init__.py']
        for f in files[:1]:
            mod = importlib.import_module(f[:-3])
            self.assertIsNotNone(mod)

if __name__ == "__main__":
    unittest.main()
