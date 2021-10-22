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
