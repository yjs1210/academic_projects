# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 00:54:47 2019

@author: James
"""
import unittest
import sys
sys.path.insert(0, '../src/')
from RDBDataTable import RDBDataTable
   
class TestStringMethods(unittest.TestCase):

   def setUp(self):
         self.cnx = {
            'host': 'localhost',
            'user': 'intro-db',
            'password': 'introdb12',
            'db': 'demographics',
            'port': 3306
               }
         
         worker= RDBDataTable('stats_by_zip',['zipcode'],self.cnx)
         worker._run_q('drop table if exists  demographics.unit_test' )
         worker._run_q('CREATE TABLE demographics.unit_test LIKE demographics.stats_by_zip')
         worker._run_q('INSERT INTO demographics.unit_test Select * from demographics.stats_by_zip' )
         self.worker_test = RDBDataTable('demographics.unit_test',['zipcode'],self.cnx)

   def test_wrong_keys_in_init_raises_error(self):
        with self.assertRaises(ValueError):
            RDBDataTable('demographics.unit_test',['zipcode','cnt_female'],self.cnx)

   def test_wrong_keys_in_query_raises_error(self):
        with self.assertRaises(ValueError):
            self.worker_test.find_by_primary_key([10003,1])
            
   def test_find_by_keys_works(self):
        self.assertEqual(self.worker_test.find_by_primary_key([10004],field_list=['zipcode'])._rows,[{'zipcode': 10004}])
            
   def test_find_by_template_works(self):
        self.assertEqual(self.worker_test.find_by_template({'zipcode': 10004},
                                                               field_list=['cnt_participants'])._rows,[{'cnt_participants': 0}])
   
   def test_none_returned_on_no_result_query(self):
        self.assertEqual(self.worker_test.find_by_primary_key([-99999]),None)
        
   def test_invalid_field_name(self):
        with self.assertRaises(ValueError):
            self.worker_test.find_by_template({'zipcode': 10004},field_list=['test'])

   def tearDown(self):
        self.worker_test._run_q('drop table if exists demographics.unit_test' )
   
if __name__ == '__main__':
    log_file = 'log_file.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f,verbosity=4)
    unittest.main(testRunner=runner)
    f.close()
    
##TEST
###User queries from a None Derived table
###User quries from a table with di