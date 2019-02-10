# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 00:54:47 2019

@author: James
"""
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
    
##TEST
###check if user entered ther right keys
#x = RDBDataTable('demographics.stats_by_zip',['zipcode','WRONG KEY'],cnx)
###check correct connection
###None value queries
###field name that is not in a dictionary
###Check if field_list filter works properly 
###Handle for query that returns no result
###User queries from a None Derived table
###User quries from a table with di