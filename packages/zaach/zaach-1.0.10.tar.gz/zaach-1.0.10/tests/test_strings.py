import os
import unittest

from zaach import strings


class StringsTestCase(unittest.TestCase):
    def test_lcut_1(self):
        s = "'foo'"
        sub = "'"
        self.assertEqual(strings.lcut(s, sub), "foo'")

    def test_lcut_2(self):
        s = ""
        sub = "'"
        self.assertEqual(strings.lcut(s, sub), "")

    def test_rcut_1(self):
        s = "'foo'"
        sub = "'"
        self.assertEqual(strings.rcut(s, sub), "'foo")

    def test_rcut_2(self):
        s = ""
        sub = "'"
        self.assertEqual(strings.rcut(s, sub), "")

    def test_cut(self):
        s = "'foo'"
        sub = "'"
        self.assertEqual(strings.cut(s, sub), "foo")

    @unittest.skip("Prints to stdout")
    def test_colors_1(self):
        print()

        for color in strings.COLORS.keys():
            print(strings.colored(text=color, color=color))

        print(strings.colored(text="", color="brightwhite"))

    def test_colors_2(self):
        self.assertEqual(
            strings.colored(text="", color="invalid"),
            strings.colored(text="", color="brightwhite"),
        )

    def test_colors_3(self):
        _pre_mock_val = os.environ.get("NO_COLOR")
        os.environ["NO_COLOR"] = ""

        self.assertEqual(strings.colored(text="text", color="red"), "text")

        if _pre_mock_val is not None:
            os.environ["NO_COLOR"] = _pre_mock_val
