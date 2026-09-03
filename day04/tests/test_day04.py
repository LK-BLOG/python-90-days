# -*- coding: utf-8 -*-
import unittest
class TestDay04(unittest.TestCase):
    def test_slice(self):
        self.assertEqual("Hello"[::-1], "olleH")
    def test_regex(self):
        import re
        m = re.search(r'\d+', "abc123def")
        self.assertEqual(m.group(), "123")
if __name__ == "__main__":
    unittest.main()
