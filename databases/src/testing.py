from BaseDataTable import BaseDataTable
from RDBDataTable import RDBDataTable
import pandas as pd
import pymysql

cnx = {
    'host': 'localhost',
    'user': 'intro-db',
    'password': 'introdb12',
    'db': 'demographics',
    'port': 3306
}

x = RDBDataTable('demographics.stats_by_zip',['zipcode','cnt_participants'],cnx)
#out = x.find_by_primary_key([10003,1], field_list= ['cnt_participants','cnt_female'])

#x.find_by_template({'zipcode':10003,'cnt_participants':1})
#out = x.find_by_primary_key([-10000,1], field_list= ['cnt_participants','cnt_female'])