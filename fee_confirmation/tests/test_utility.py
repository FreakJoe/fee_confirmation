import unittest

from ..utility import is_power_of

class TestUtilityFunctions(unittest.TestCase):
	def test_power_of(self):
		self.assertTrue(is_power_of(2, 4))
		self.assertTrue(is_power_of(2, 8))
		self.assertTrue(is_power_of(2, 1024))
		self.assertTrue(is_power_of(10, 100000))
		self.assertTrue(is_power_of(10, 1000))
		self.assertTrue(is_power_of(3, 27))

		self.assertFalse(is_power_of(2, 5))
		self.assertFalse(is_power_of(10, 90))
		self.assertFalse(is_power_of(35, 90))
		self.assertFalse(is_power_of(2, 10))
		self.assertFalse(is_power_of(7, 48))