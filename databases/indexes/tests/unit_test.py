import sys
sys.stdout = open('test_output/rest_log.txt', 'w+')
print('test')
from src import CSVDataTable
import csv
import json
import logging 
import time

logging.basicConfig(level=logging.INFO)

def load(fn):

    result = []
    cols = None
    with open(fn, "r") as infile:
        rdr = csv.DictReader(infile)
        cols = rdr.fieldnames
        for r in rdr:
            result.append(r)

    return result, cols

def test_load():
    rows, cols = load("indexes/CSVFile/people.csv")
    print(rows)

test_load()



