import unittest
from parameterized import parameterized
from session1.class_to_test import ClassToTest


class TestClassToTest(unittest.TestCase):

    def setUp(self) -> None:
        self.class_to_test = ClassToTest()

    @parameterized.expand([
        [1, 8],
        [4, 13],
        [16, 236],
    ])
    def test_call_perfect_square(self, num_true, num_false):
        assert self.class_to_test.call_perfect_square(num_true) is True
        assert self.class_to_test.call_perfect_square(num_false) is False
