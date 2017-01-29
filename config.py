import os
import math

# Edit this to your liking
DATA_FOLDER = 'data' # Name of the folder (inside of the root application directory) that will hold data
CSV_NAME = 'conf_times.csv' # Name of the csv file holding the data (inside of the data folder)
TEST_CSV_NAME = 'test_conf_times.csv'

AXIS_BASE = 2
MAX_FEE_RATE = 256 # Must be a multiple of AXIS_BASE
MAX_CONFIRMATION_BLOCKS = 256 # Must be a multiple of AXIS_BASE

# Don't edit this
RATE_EXPONENT = int(math.ceil(math.log(MAX_FEE_RATE, AXIS_BASE)))
BLOCK_EXPONENT = int(math.ceil(math.log(MAX_CONFIRMATION_BLOCKS, AXIS_BASE)))
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, DATA_FOLDER)
CSV_PATH = os.path.join(DATA_PATH, CSV_NAME)
TEST_CSV_PATH = os.path.join(DATA_PATH, TEST_CSV_NAME)