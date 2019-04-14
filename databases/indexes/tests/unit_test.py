##James Lee - jl5241
import sys
sys.stdout = open('test_output/rest_log.txt', 'w+')
from src import CSVDataTable
import csv
import json
import logging 
import time
print("##James Lee - jl5241\n")
print("************************************************************\n")


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

def test_insert_and_import():
    print("\n\n*************TEST ONE, TEST LOAD FUNCTIOn**************")
    rows, cols = load("CSVFile/people.csv")
    t=CSVDataTable.CSVDataTable(table_name = "People",column_names = cols, primary_key_columns=['playerID'])
    t.import_data(rows)
    print("T = ",t)

def test_find():
    print("\n\n*************TEST TWO,  FIND BY TEMPLATE AND COMPARE RUN TIME WITH INDEX vs WITHOUT**************")
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
    print("\n\n*************TEST THREE CREATING A CSVDATATABLE OBJECT**************")
    t = CSVDataTable.CSVDataTable(table_name="Test",column_names=['foo','bar'],primary_key_columns=['foo'],loadit=None)
    print("T = ",t)

def test_index():
    print("\n\n*************TEST FOUR CREATING AN INDEX**************")
    t = CSVDataTable.CSVDataTable(table_name="Test",column_names=['last_name','first_name','uni'],loadit=None)
    i = CSVDataTable.Index(index_name="Bob", index_columns = ["last_name","first_name"],kind="INDEX", table = t)
    print(i)
    r = {"last_name": "Ferguson", "first_name": "Donald", "uni":"sure"}
    kv = i.compute_key(r)
    i.add_to_index(row=r,rid="2")
    print("KV = ",kv, "added to index")

def test_conflict():
    print("\n\n*************TEST FIVE CREATING CONFLICTING INDEX THROWS ERROR WHEN UNIQUE**************")
    t= CSVDataTable.CSVDataTable(table_name="Test",column_names=['last_name','first_name','uni'],loadit=None)
    i = CSVDataTable.Index(index_name="Bob", index_columns = ["last_name","first_name"],kind="UNIQUE",table=t)
    r = {"last_name": "Ferguson", "first_name": "Donald", "uni":"sure"}
    kv = i.compute_key(r)
    i.add_to_index(row=r,rid="2")
    try:
        i.add_to_index(row=r, rid="3")
    except Exception as e:
        print("We caught an error: ", e)

def test_add_index():
    print("\n\n*************TEST SIX, CREATE WITH INDEX AND THEN ADD ANOTHER INDEX**************")
    rows, cols = load("CSVFile/offices.csv")
    t=CSVDataTable.CSVDataTable(table_name = "Offices",column_names = cols, primary_key_columns=["officeCode"])
    print("\n***ORIGINALLY ***\n")
    print(t)
    cols = ["city","state","postalCode"]
    t.add_index(name="location",column_list=cols,kind="INDEX")
    print("\n***ADDING ANOTHER INDEX, LOCATION ***\n")
    print(t)

def test_duplicate_index_name():
    print("\n\n*************TEST SEVEN, CREATING AN INDEX WITH A DUPLICATE NAME, AND CREATING A SECOND PRIMARY KEY THROWS AN ERROR**************")
    rows, cols = load("CSVFile/offices.csv")
    t=CSVDataTable.CSVDataTable(table_name = "Offices",column_names = cols, primary_key_columns=["officeCode"])
    print("\n***ORIGINAL ***\n")
    print(t)
    cols = ["city","state","postalCode"]
    try:
        t.add_index("PRIMARY",['city'],"INDEX")
    except Exception as e:
        print("*****You tried to add a duplicate name index*****"+ "\n",e)
    try:
        t.add_index("RANDOM",['state'],"PRIMARY")
    except Exception as e:
        print("\n*****You tried to make more than one primary keys*****"+ "\n",e)

def test_incomplete_index_info():
    ###CHECK FOR not complete index info ADD_INDEX FUNCTION 
    print("\n\n*************TEST SIX, CREATE WITH INDEX AND ADD ANOTHER INDEX**************")
    rows, cols = load("CSVFile/offices.csv")
    t=CSVDataTable.CSVDataTable(table_name = "Offices",column_names = cols, primary_key_columns=["officeCode"])
    cols = ["city","state","postalCode"]
    try:
        t.add_index("location",cols)
    except Exception as e:
        print("\n We caught an error, you did  not provide enough information to create the key" + "\n",e)


def test_specific_project():
    rows, cols = load("CSVFile/People.csv")
    t=CSVDataTable.CSVDataTable(table_name = "People",column_names = cols, primary_key_columns=["playerID"])
    t.import_data(rows)
    print("T = ",t)

    p = ["playerID","People.nameLast","Batting.H"]
    print("Specific template = ", t._get_specific_project())

def test_join():
    ###CHECK FOR not complete index info ADD_INDEX FUNCTION 
    print("*************TEST SIX JOIN AND ALSO SEE THAT IT SWAPS TABLESX**************")
    rows, cols = load("CSVFile/People.csv")
    t=CSVDataTable.CSVDataTable(table_name = "People",column_names = cols, primary_key_columns=["playerID"])
    t.import_data(rows)
    print("T = ",t)

    rows, cols = load("CSVFile/Batting.csv")
    t2=CSVDataTable.CSVDataTable(table_name = "Batting",column_names = cols, primary_key_columns=["playerID","teamID","yearID","stint"])
    t2.import_data(rows)
    print("T2 = ",t2)

    j = t2.join(t, ['playerID'],
        w_cluase ={"People.nameLast":"Williams", "People.birthCity": "San Diego"},
        p_clause =['playerID',"People.nameLast","People.nameFirst","Batting.teamID","Batting.yearID","Batting.stint","Batting.H","Batting.AB"]
        ,optimize = True)

    print("Result = " ,j)
    print("All rows = ", json.dumps(j._rows, indent=2))


def test_delete():
    print("*************TEST SIX, CREATE WITH INDEX AND ADD ANOTHER INDEX**************")
    rows, cols = load("CSVFile/offices.csv")
    t=CSVDataTable.CSVDataTable(table_name = "Offices",column_names = cols, primary_key_columns=["officeCode"])

    t.import_data(rows)

    r = t.delete({"city":"Cambridge"})
    print(t)



test_insert_and_import()
test_init()
test_index()
test_conflict()
test_add_index()
test_duplicate_index_name()
test_incomplete_index_info()

