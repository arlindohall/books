#!/bin/bash

# Read in ISBNs from a barcode scanner
dd >> content/input.txt

# From the scanned ISBNs, search each entry and put the result in a
# pre-defined blob file that contains newline-separated JSON blobs
# (maybe make this a database later...)
python scan_books.py < content/input.txt

# Create a CSV (much quicker than step 2)
python classify_books.py < content/blobs.txt > content/output.csv
