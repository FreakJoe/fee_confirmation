import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker

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

	# Populate X, Y, Z as per documentation on matplotlib.pyplot.pcolor
	distribution = [[0 for j in range(RATE_EXPONENT + 2)] for i in range(BLOCK_EXPONENT + 2)]
	x = [[0 for j in range(RATE_EXPONENT + 2)] for i in range(BLOCK_EXPONENT + 2)]
	y = [[0 for j in range(RATE_EXPONENT + 2)] for i in range(BLOCK_EXPONENT + 2)]
	total_transactions = len(data)
	for i in range(BLOCK_EXPONENT + 2):
		block_min = 0
		if i != 0:
			block_min = AXIS_BASE ** (i - 1)

		block_max = 1
		if i != 0:
			block_max = AXIS_BASE ** (i)

		for j in range(RATE_EXPONENT + 2):
			rate_min = 0
			if j != 0:
				rate_min = AXIS_BASE ** (j - 1)

			rate_max = 1
			if j != 0:
				rate_max = AXIS_BASE ** (j)

			x[i][j] = rate_min
			try:
				x[i][j + 1] = rate_max

			except:
				pass

			y[i][j] = block_min
			try:
				[i + 1][j] = block_max

			except:
				pass

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

			percentage = float(len(transactions_grid)) / float(total_transactions)
			distribution[i][j] = percentage

	# Convert 2-dimensional list to np array
	return (np.array(x), np.array(y), np.array(distribution))

def draw():
	"""Draws the plot"""
	(X, Y, Z) = calculate_distribution()
	if not Z.any():
		return

	fig, ax = plt.subplots()
	ax.set_xbound(0.0, MAX_FEE_RATE)
	ax.set_ybound(0.0, MAX_CONFIRMATION_BLOCKS)
	ax.set_xlabel('Fee rate in satoshis / byte')
	ax.set_ylabel('Confirmation time in blocks')
	ax.set_xscale('symlog')
	ax.set_yscale('symlog')
	ax.set_xticks(X[0])
	ax.set_yticks(X[0])
	ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
	ax.get_yaxis().set_major_formatter(ticker.ScalarFormatter())

	colour_map = colors.LinearSegmentedColormap.from_list('GreenRed', ['red', 'green'], N=256)
	img = ax.pcolormesh(X, Y, Z, cmap=colour_map)
	plt.colorbar(img, cmap=colour_map)
	plt.show()

	return

def plot():
	"""Create a colour-coded plot displaying the distribution of bitcoin transactions' fee rate
	and their confirmation time in blocks"""
	draw()