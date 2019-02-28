# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 00:54:47 2019

@author: James
"""
import unittest
import sys
from shutil import copyfile
import os
sys.path.insert(0, '../src/')
from CSVDataTable import CSVDataTable
   
class TestStringMethods(unittest.TestCase):

   def setUp(self):
         connect_info = {
                'directory': '../data/',
                'file_name': 'demographics_by_zip.csv'
            }
       
         self.cnx = {
                'directory': '../data/',
                'file_name': 'unit_test_temp.csv'
            }        
        
         copyfile(connect_info['directory'] + connect_info['file_name'], connect_info['directory'] + 'unit_test_temp.csv')
         
         self.worker_test= CSVDataTable('stats_by_zip_test',connect_info=self.cnx,key_columns=['zipcode'])      
         self.worker_test.load()

   def test_wrong_keys_in_query_raises_error(self):
        with self.assertRaises(ValueError):
            self.worker_test.find_by_primary_key([10003,1])
            
   def test_find_by_keys_works(self):
        self.assertEqual(self.worker_test.find_by_primary_key(['10004'],field_list=['zipcode'])._rows,[{'zipcode': '10004'}])
            
   def test_find_by_template_works(self):
        self.assertEqual(self.worker_test.find_by_template({'zipcode': '10004'},
                                                              field_list=['cnt_participants'])._rows,[{'cnt_participants': '0'}])
   
   def test_delete_by_template_works(self):
        self.worker_test.delete_by_template({'zipcode': '10007'})
        out = self.worker_test.find_by_template({'zipcode': '10007'})
        self.assertEqual(None, out)
        
   def test_delete_by_key_works(self):
        self.worker_test.delete_by_key(['10005'])
        out = self.worker_test.find_by_primary_key(['10005'])
        self.assertEqual(None, out)
    
   def test_update_by_template_works(self):
        self.worker_test.update_by_template({'zipcode': '10006'},{'cnt_participants':'3'})
        out = self.worker_test.find_by_template({'zipcode': '10006'},field_list=['cnt_participants'])
        self.assertEqual([{'cnt_participants': '3'}], out._rows)
              
   def test_update_by_key_works(self):
        self.worker_test.update_by_key(['10006'],{'cnt_participants':'6'})
        out = self.worker_test.find_by_primary_key(['10006'],field_list=['cnt_participants'])
        self.assertEqual([{'cnt_participants': '6'}], out._rows)
        
   def test_none_returned_on_no_result_query(self):
        self.assertEqual(self.worker_test.find_by_primary_key(['-99999']),None)
        
   def test_invalid_field_name(self):
        with self.assertRaises(ValueError):
            self.worker_test.find_by_template({'zipcode': '10004'},field_list=['test'])

   def test_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.worker_test.find_by_template({'zipcode': '10004'},field_list=['zipcode']).find_by_primary_key([-99999])

   def tearDown(self):
        os.remove(self.cnx['directory'] + self.cnx['file_name'])
   
if __name__ == '__main__':
    log_file = 'csv_table_test.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f,verbosity=4)
    unittest.main(testRunner=runner)
    f.close()
    
##TEST
###User queries from a None Derived table
###User quries from a table with di