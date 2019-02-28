# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 00:54:47 2019

@author: James
"""
import unittest
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
        self.assertEqual(self.worker_test.find_by_primary_key([10004],field_list=['zipcode'])._rows,
                         self.worker_test._run_q("Select zipcode from demographics.unit_test where zipcode = 10004"))
            
   def test_find_by_template_works(self):
        self.assertEqual(self.worker_test.find_by_template({'zipcode': 10004},
                                                              field_list=['cnt_participants'])._rows,[{'cnt_participants': 0}])
   
   def test_delete_by_template_works(self):
        self.worker_test.delete_by_template({'zipcode': 10004})
        out = self.worker_test.find_by_template({'zipcode': 10004})
        self.assertEqual(None, out)
        
   def test_delete_by_key_works(self):
        self.worker_test.delete_by_key([10005])
        out = self.worker_test.find_by_primary_key([10005])
        self.assertEqual(None, out)
    
   def test_update_by_template_works(self):
        self.worker_test.update_by_template({'zipcode': 10006},{'cnt_participants':3})
        out = self.worker_test.find_by_template({'zipcode': 10006},field_list=['cnt_participants'])
        self.assertEqual([{'cnt_participants': 3}], out._rows)
              
   def test_update_by_key_works(self):
        self.worker_test.update_by_key([10006],{'cnt_participants':6})
        out = self.worker_test.find_by_primary_key([10006],field_list=['cnt_participants'])
        self.assertEqual([{'cnt_participants': 6}], out._rows)
        
   def test_none_returned_on_no_result_query(self):
        self.assertEqual(self.worker_test.find_by_primary_key([-99999]),None)
        
   def test_invalid_field_name(self):
        with self.assertRaises(ValueError):
            self.worker_test.find_by_template({'zipcode': 10004},field_list=['test'])
            
   def test_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.worker_test.find_by_template({'zipcode': 10004},field_list=['zipcode']).find_by_primary_key([-99999])

   def tearDown(self):
        self.worker_test._run_q('drop table if exists demographics.unit_test' )
   
if __name__ == '__main__':
    unittest.main()
    log_file = 'rdb_table_test.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f,verbosity=4)
    unittest.main(testRunner=runner)
    f.close()
    
    ##TEST
    ###User queries from a None Derived table
    ###User quries from a table with di