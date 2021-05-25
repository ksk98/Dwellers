import unittest
from network import utility


class TestsNetwork(unittest.TestCase):
    def test_utility_get_value_of_argument(self):
        header = (
                    "ARGUMENT-FIRST: BAD\r\n"
                    "ARGUMENT-SECOND: GOOD\r\n"
                    "ARGUMENT-THIRD: BAD\r\n"
        )

        self.assertNotEqual(utility.get_value_of_argument(header, "ARGUMENT-FIRST"), "GOOD")
        self.assertEqual(utility.get_value_of_argument(header, "ARGUMENT-SECOND"), "GOOD")
        self.assertEqual(utility.get_value_of_argument(header, "ARGUMENT-FOURTH"), "")

    def test_hh(self):
        dictt = {13: "hehe"}
        self.assertEqual(list(dictt.keys())[list(dictt.values()).index("hehe")], 13)
        if "hehi" in dictt.values():
            self.assertEqual(list(dictt.keys())[list(dictt.values()).index("hehi")], None)
