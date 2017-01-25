import os

# Edit this to your liking
DATA_FOLDER = 'data' # Name of the folder (inside of the root application directory) that will hold data
CSV_NAME = 'conf_times.csv' # Name of the csv file holding the data (inside of the data folder)

# Don't edit this
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, DATA_FOLDER)
CSV_PATH = os.path.join(DATA_PATH, CSV_NAME)