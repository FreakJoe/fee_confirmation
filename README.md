# Fee Confirmation

## Purpose

This project is intended to provide a visual (colour-map based) visualization of the connection between a bitcoin transaction's fee rate and the amount of blocks it took for the transaction to be confirmed.

## Setup

1) Adjust the values in config.py to your liking.

2) Provide a data file (.csv) of the specified name in the specified data directory. It should, at the very least, contain the rows 'fee_rate' (in satoshis / byte) and 'conf_blocks' (number of blocks the transaction took to confirm).

3) Install all necessary dependencies via "pip install -r requirements.txt"

4) Run "python run.py"