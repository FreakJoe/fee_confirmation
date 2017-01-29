import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import math

from config import CSV_PATH, MAX_FEE_RATE, MAX_CONFIRMATION_BLOCKS, AXIS_BASE, RATE_EXPONENT, BLOCK_EXPONENT
from .utility import is_power_of

def calculate_distribution():
	"""Calculates the percentage of transactions located within each grid"""
	data = None
	try:
		data = pd.read_csv(CSV_PATH, usecols=['fee_rate', 'conf_blocks'])

	except:
		print('Make sure you\'ve supplied a correctly named data file in the place specified in config.py')
		return

	data = data.sort_values('fee_rate', ascending=True)

	# Ensure that the max values of the axes are powers of AXIS_BASE
	if not is_power_of(AXIS_BASE, MAX_FEE_RATE) or not is_power_of(AXIS_BASE, MAX_CONFIRMATION_BLOCKS):
		print('Ensure that both the max fee rate and max number of confirmation blocks are powers of 10')
		raise ValueError

	distribution = []
	# Initialize the distribution dict to contain a sub-dict
	# For each grid along the x (fee rate) and within those sub-dicts another
	# sub-dict for every grid along the y axis (blocks to confirm)
	for i in range(BLOCK_EXPONENT + 1):
		distribution.append([])
		for n in range(RATE_EXPONENT + 1):
			distribution[i].append(float(i) / float(BLOCK_EXPONENT))

	# Convert 2-dimensional list to np array and reverse to account for the first sub-list representing
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
	ax.pcolorfast(x_edges, y_edges, distribution, cmap=colour_map)
	plt.show()

	return

def plot():
	"""Create a colour-coded plot displaying the distribution of bitcoin transactions' fee rate
	and their confirmation time in blocks"""
	draw()