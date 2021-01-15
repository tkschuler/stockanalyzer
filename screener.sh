#!/bin/bash

# TODO if .env exists then activate, otherwise warn

python3 -u AutoDD_Rev2/main.py --csv --yahoo --interval 48
python3 redditfilter.py
