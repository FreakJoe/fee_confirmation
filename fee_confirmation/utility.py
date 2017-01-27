from math import log

def is_power_of(base, potential_power):
	"""Tests whether a number is a power of any given base"""
	# Avoid weird floating point errors
	lg = round(log(potential_power, base), 4)
	
	return lg.is_integer()