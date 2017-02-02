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

		# Ensure that there is one grid containing 20% and two containing 40% of transactions
		self.assertEqual(np.count_nonzero(distribution.flatten() == 0.2), 1)
		self.assertEqual(np.count_nonzero(distribution.flatten() == 0.4), 2)