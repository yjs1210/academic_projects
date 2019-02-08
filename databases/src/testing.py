from BaseDataTable import BaseDataTable
from RDBDataTable import RDBDataTable
import pandas as pd
import pymysql

cnx = {
    'host': 'localhost',
    'user': 'yjs1210',
    'password': '@Wjdtjr12',
    'db': 'demographics',
    'port': 3306
}

x = RDBDataTable('demographics.stats_by_zip',['zipcode','cnt_participants'],cnx)


x.update_by_key( [10002,35] ,{'zipcode':10003 ,'cnt_participants':1})