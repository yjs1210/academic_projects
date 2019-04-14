import CSVDataTableNew as CSVD
import logging
import csv

def load(fn):
    result = []
    cols = None
    with open(fn, "r") as infile:
        rdr = csv.DictReader(infile)
        cols = rdr.fieldnames
        for r in rdr:
            result.append(r)

    return result, cols


def t1():
    t = CSVD.CSVDataTable(table_name='Test', column_names=['foo', 'bar'], primary_key_columns=['foo'], loadit=None)
    print("T = ", t)

def t2():

    new_r, cols = load('/Users/yimin/Desktop/Columbia/Spring 2019/Databases/HW3/student.csv')
    t = CSVD.CSVDataTable(table_name='student',
                                  column_names=cols,
                                  primary_key_columns=['uni'],
                                  loadit=None)
    t.import_data(new_r)
    print("T = ", t)

def t3():
    new_r, cols = load('/Users/yimin/Desktop/Columbia/Spring 2019/Databases/HW3/student.csv')
    t = CSVD.CSVDataTable(table_name='student',
                                  column_names=cols,
                                  primary_key_columns=['uni'],
                                  loadit=None)
    t.import_data(new_r)
    t.save()

def t4():
    t = CSVD.CSVDataTable(table_name='student', loadit=True)
    print("T = ", t)

def t5():
    t = CSVD.CSVDataTable(table_name='student', loadit=True)
    new_r, cols = load('/Users/yimin/Desktop/Columbia/Spring 2019/Databases/HW3/student.csv')
    s = CSVD.CSVDataTable(table_name='student',
                                  column_names=cols,
                                  primary_key_columns=['uni'],
                                  loadit=None)
    s.import_data(new_r)
    print("T = ", t)
    print("S = ", s)


#t1()
#t2()
#t3()
#t4()
t5()