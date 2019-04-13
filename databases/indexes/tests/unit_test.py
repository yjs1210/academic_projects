import sys
sys.stdout = open('test_output/rest_log.txt', 'w+')
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
    rows, cols = load("CSVFile/people.csv")
    t=CSVDataTable.CSVDataTable(table_name = "People",column_names = cols, primary_key_columns=['playerID'])
    t.import_date(rows)
    print("T = ",t)

def test_find():
    tmp = {"playerID":"willite01"}

    start = time.time()
    for i in range(0,1000):
        r = t.find_by_template(tmp,fields=None,use_index=False)
        if i ==0:
            print("Row = ",r)
    end = time.time()
    elapsed = end - start
    print("Elapsed time=", elapsed)

    start = time.time()
    for i in range(0,1000):
        r=t.find_by_template(tmp,fields=None,use_index=True)
        if i==0:
            print("Row = ",r)
    end = time.time()
    elapsed = end-start
    print("Elapsed time = ",elapsed)


def test_init():
    t = CSVDataTable.CSVDataTable(table_name="Test",column_names=['foo','bar'],primary_key_columns=['foo'],loadit=None)
    print("T = ",t)

def test_index():
    i = CSVDataTable.Index(index_name="Bob", index_columns = ["last_name","first_name"],kind="INDEX")
    r = {"last_name" :"Ferguson", "first_name": "Donald", "uni":"sure"}
    kv = i.compute_key(r)
    print("KV = ",kv)


test_load()
test_init()



