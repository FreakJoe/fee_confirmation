import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from config import CSV_PATH, MAX_FEE_RATE, MAX_CONFIRMATION_BLOCKS
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

	# Ensure that the max values of the axes are powers of 10
	if not is_power_of(10, MAX_FEE_RATE) or not is_power_of(10, MAX_CONFIRMATION_BLOCKS):
		print('Ensure that both the max fee rate and max number of confirmation blocks are powers of 10')
		raise ValueError

	distribution = {}
	# Initialize the distribution dict to contain a sub-dict
	# For each grid along the x (fee rate) and within those sub-dicts another
	# sub-dict for every grid along the y axis (blocks to confirm)
	for i in range(int(np.log10(MAX_FEE_RATE)) + 1):
		distribution[str(i)] = {}
		if i != 0:
			distribution[str(i)]['min_fee_rate'] = 10 ** (i - 1)

		else:
			distribution[str(i)]['min_fee_rate'] = 0

		distribution[str(i)]['max_fee_rate'] = 10 ** i

		for n in range(int(np.log10(MAX_FEE_RATE)) + 1):
			distribution[str(i)][str(n)] = {}
			if n != 0:
				distribution[str(i)][str(n)]['min_conf_blocks'] = 10 ** (n - 1)

			else:
				distribution[str(i)][str(n)]['min_conf_blocks'] = 0

			distribution[str(i)][str(n)]['max_conf_blocks'] = 10 ** n
			distribution[str(i)][str(n)]['percentage'] = None

	return distribution

def draw():
	"""Draws the plot"""

	fig, ax = plt.subplots()
	Z = np.random.random(size=(4, 4))
	x_edges = [0] + [10 ** i for i in range(int(np.log10(MAX_FEE_RATE)) + 1)]
	y_edges = [0] + [10 ** i for i in range(int(np.log10(MAX_CONFIRMATION_BLOCKS)) + 1)]
	X, Y = np.meshgrid(x_edges, y_edges)
	ax.set_xbound(0.0, MAX_FEE_RATE)
	ax.set_ybound(0.0, MAX_CONFIRMATION_BLOCKS)
	ax.set_xlabel('Fee rate in satoshis / byte')
	ax.set_ylabel('Confirmation time in blocks')

	colour_map = colors.LinearSegmentedColormap.from_list('GreenRed', ['red', 'green'], N=256)
	ax.pcolorfast(X, Y, Z, cmap=colour_map)
	plt.show()

	return

def plot():
	"""Create a colour-coded plot displaying the distribution of bitcoin transactions' fee rate
	and their confirmation time in blocks"""
	distribution = calculate_distribution()
	draw()