# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 00:54:47 2019

@author: James
"""
import unittest
import sys
sys.path.insert(0, '../src/')
from TenGreatestHitters import TenGreatestHitters
   
class TestStringMethods(unittest.TestCase):
   
   def setUp(self):
        self.x = TenGreatestHitters()

   def test_people_load_done(self):
        self.assertEqual(len(self.x._people) >0, True)
       
   def test_batting_load_done(self):
        self.assertEqual(len(self.x._batting) >0, True)
    
   def test_aggregate_computed_correctly(self):
        out2 = self.x.compute_aggs_and_year_by_id(['AB','H'])
        self.assertEqual(round(out2['willite01']['H'],1),2654.0)
            
   def test_average_calculated_correctly(self):
        out2 = self.x.compute_aggs_and_year_by_id(['AB','H'])
        out3 = self.x.compute_batting_avg(out2)
        self.assertEqual(round(out3['willite01']['batting_avg'],4),0.3444)
            
   def test_filtered_correctly(self):
        out2 = self.x.compute_aggs_and_year_by_id(['AB','H'])
        out3 = self.x.compute_batting_avg(out2)
        out4 = self.x.filter_AB_by_at_least_value(out3,200,1960)
        self.assertEqual(any(v['AB'] < 200  for v in out4.values()),False)
   
   def test_sort_by_field_correctly(self):
        out2 = self.x.compute_aggs_and_year_by_id(['AB','H'])
        out3 = self.x.compute_batting_avg(out2)
        out4 = self.x.filter_AB_by_at_least_value(out3,200,1960)
        out5 = self.x.sort_by_field(out4,'batting_avg')
        self.assertEqual(out5[0][1]['batting_avg']>=out5[1][1]['batting_avg'],True)
        
   def test_invalid_field_name(self):
        out2 = self.x.compute_aggs_and_year_by_id(['AB','H'])
        out3 = self.x.compute_batting_avg(out2)
        out4 = self.x.filter_AB_by_at_least_value(out3,200,1960)
        out5 = self.x.sort_by_field(out4,'batting_avg')
        out6 = self.x.join_people(out5)
        self.assertEqual('first_name' in out6[0][1], True)
   
if __name__ == '__main__':
    log_file = 'TenGreatestHittersTest.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f,verbosity=4)
    unittest.main(testRunner=runner)
    f.close()
    
##TEST
###User queries from a None Derived table
###User quries from a table with di