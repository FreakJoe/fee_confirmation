import unittest
import os
import sys
import numpy as np

sys.path.insert(0, os.getcwd())

from config import BLOCK_EXPONENT, RATE_EXPONENT
from ..plot import calculate_distribution

class TestPlot(unittest.TestCase):
	def test_distribution(self):
		distribution = calculate_distribution(test=True)[2]
		for a in distribution:
			self.assertEqual(len(a), RATE_EXPONENT + 2)

		for j in range(0, len(distribution[0])):
			cumulative_percentage = 0
			for i in range(0, len(distribution)):
				cumulative_percentage += distribution[i, j]

			if cumulative_percentage != 0:
				self.assertAlmostEqual(cumulative_percentage, 1, places=3)