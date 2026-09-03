# -*- coding: utf-8 -*-
# Day 1 测试
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'starter'))


class TestShowPrice(unittest.TestCase):
    """测试show_price函数"""

    def test_basic(self):
        from importlib import import_module
        mod = import_module("01_basics_practice")
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            mod.show_price("iPhone", 5999)
        output = f.getvalue()
        self.assertIn("iPhone", output)
        self.assertIn("5999", output)


class TestAverage(unittest.TestCase):
    """测试average函数"""

    def test_basic(self):
        from importlib import import_module
        mod = import_module("02_args_practice")
        self.assertAlmostEqual(mod.average(1, 2, 3), 2.0)

    def test_single(self):
        from importlib import import_module
        mod = import_module("02_args_practice")
        self.assertAlmostEqual(mod.average(5), 5.0)

    def test_many(self):
        from importlib import import_module
        mod = import_module("02_args_practice")
        self.assertAlmostEqual(mod.average(10, 20, 30, 40, 50), 30.0)

    def test_float(self):
        from importlib import import_module
        mod = import_module("02_args_practice")
        self.assertAlmostEqual(mod.average(1.5, 2.5, 3.0), 2.3333333333, places=5)


class TestGreet(unittest.TestCase):
    """测试greet函数"""

    def test_default_greeting(self):
        from importlib import import_module
        mod = import_module("01_basics_practice")
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            mod.greet("小明")
        self.assertIn("你好", f.getvalue())

    def test_custom_greeting(self):
        from importlib import import_module
        mod = import_module("01_basics_practice")
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            mod.greet("小明", "早上好")
        self.assertIn("早上好", f.getvalue())


if __name__ == "__main__":
    unittest.main()
