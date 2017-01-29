import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import math

from config import CSV_PATH, TEST_CSV_PATH, MAX_FEE_RATE, MAX_CONFIRMATION_BLOCKS, AXIS_BASE, RATE_EXPONENT, BLOCK_EXPONENT
from .utility import is_power_of

def calculate_distribution(test=False):
	"""Calculates the percentage of transactions in each grid"""
	data = None
	try:
		if not test:
			data = pd.read_csv(CSV_PATH, usecols=['fee_rate', 'conf_blocks'])

		else:
			data = pd.read_csv(TEST_CSV_PATH, usecols=['fee_rate', 'conf_blocks'])

	except:
		print('Make sure you\'ve supplied a correctly named data file in the place specified in config.py')
		return

	data = data.sort_values('fee_rate', ascending=True)

	# Ensure that the max values of the axes are powers of AXIS_BASE
	if not is_power_of(AXIS_BASE, MAX_FEE_RATE) or not is_power_of(AXIS_BASE, MAX_CONFIRMATION_BLOCKS):
		print('Ensure that both the max fee rate and max number of confirmation blocks are powers of 10')
		raise ValueError

	distribution = []
	total_transactions = len(data)
	# Calculate distribution
	# Each sub-list is a range of blocks it took to confirm
	# Each sub-list item shows the percentage of transactions in a certain fee and conf block range
	for i in range(BLOCK_EXPONENT + 1):
		distribution.append([])
		for n in range(RATE_EXPONENT + 1):
			block_min = 0
			if i != 0:
				block_min = AXIS_BASE ** (i - 1)

			block_max = 1
			if i != 0:
				block_max = AXIS_BASE ** (i)

			rate_min = 0
			if n != 0:
				rate_min = AXIS_BASE ** (n - 1)

			rate_max = 1
			if n != 0:
				rate_max = AXIS_BASE ** (n)

			# Select transactions confirmed in less than or equal to block_max
			transactions_grid = data[data['conf_blocks'] <= block_max]
			# ... confirmed in more than block_min
			transactions_grid = transactions_grid[data['conf_blocks'] > block_min]
			# ... at a fee rate less than or equal to rate_max
			transactions_grid = transactions_grid[data['fee_rate'] <= rate_max]
			# Avoid filtering out transactions at 0 fee
			if rate_min != 0:
				# ... at a fee rate higher than rate_min
				transactions_grid = transactions_grid[data['fee_rate'] > rate_min]

			distribution[i].append(float(len(transactions_grid)) / float(total_transactions))

	# Convert 2-dimensional list to np array and reverse to account for the first sub-array representing
	# The top row of grids
	return np.array(distribution)[::-1]

def draw():
	"""Draws the plot"""
	distribution = calculate_distribution()
	if not distribution.any():
		return

	fig, ax = plt.subplots()
	x_edges = [0] + [AXIS_BASE ** i for i in range(RATE_EXPONENT + 1)]
	y_edges = [0] + [AXIS_BASE ** i for i in range(BLOCK_EXPONENT + 1)]
	ax.set_xbound(0.0, MAX_FEE_RATE)
	ax.set_ybound(0.0, MAX_CONFIRMATION_BLOCKS)
	ax.set_xlabel('Fee rate in satoshis / byte')
	ax.set_ylabel('Confirmation time in blocks')
	ax.set_xscale('symlog')
	ax.set_yscale('symlog')
	ax.set_xticks(x_edges)
	ax.set_yticks(y_edges)
	ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
	ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter())

	colour_map = colors.LinearSegmentedColormap.from_list('GreenRed', ['red', 'green'], N=256)
	img = ax.pcolorfast(x_edges, y_edges, distribution, cmap=colour_map)
	plt.colorbar(img, cmap=colour_map)
	plt.show()

	return

def plot():
	"""Create a colour-coded plot displaying the distribution of bitcoin transactions' fee rate
	and their confirmation time in blocks"""
	draw()