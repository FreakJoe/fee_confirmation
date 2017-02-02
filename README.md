# Fee Confirmation

## Purpose

This project is intended to provide a visual (colour-map based) visualization of the connection between a bitcoin transaction's fee rate and the amount of blocks it took for the transaction to be confirmed.

## Setup

1. Adjust the values in config.py to your liking.

2. Provide a data file (.csv) of the specified name in the specified data directory. It should, at the very least, contain the rows 'fee_rate' (in satoshis / byte) and 'conf_blocks' (number of blocks the transaction took to confirm).

3. Install all necessary dependencies via "pip install -r requirements.txt"

4. Run "python run.py"

## Results

Given a valid and properly configured .csv file containing transaction data, this software will output a colour-map based grid plot plotting the transactions' confirmation time in blocks against their fee rate in satoshi per byte. A grid's colour is based on the fraction that transactions contained in that grid (characterized by fee range and block range) make up of all transactions in that fee range (or of the entirety of transactions visualized in the plot, if so defined in the config). If all transactions within a given fee range were confirmed in the same block range, that grid will show as entirely green with a value of 1. A grid containing none of the transactions in that fee range will show as completely red with a value of 0.