import unittest


class TestAssertWorks(unittest.TestCase):

    def test_assert_equals(self):
        self.assertEquals(100, 100, '100 == 100')

    def test_assert_true(self):
        self.assertTrue(100 > 1, '100 > 1')
