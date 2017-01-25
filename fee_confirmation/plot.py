import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config import CSV_PATH

def plot():
	"""Create a colour-coded plot displaying the distribution of bitcoin transactions' fee rate
	and their confirmation time in blocks"""
	data = None
	try:
		data = pd.read_csv(CSV_PATH, usecols=['fee_rate', 'conf_blocks'])

	except:
		print('Make sure you\'ve supplied a correctly named data file in the place specified in config.py')

	data = data.sort_values('fee_rate', ascending=True)