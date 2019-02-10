# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:10:10 2019

@author: James
"""

import numpy as np
import csv as csv
from collections import OrderedDict as od
from operator import itemgetter
from itertools import groupby

class TenGreatestHitters():
    
    
    _default_connect_info = {
    'directory': '../data/'
    }
    
    def __init__(self,connect_info= None):
        """

        :param table_name: The name of the RDB table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """
        # Initialize and store information in the parent class.
        self._connect_info = connect_info
       
        if connect_info is None:
            self._connect_info = TenGreatestHitters._default_connect_info           
        self._people = self.load('people.csv')
        self._batting = self.load('batting.csv')
        self._debug = None
  
    def load(self, name):
        path = self._connect_info['directory'] + name
        out =[]
        with open(path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                out.append(row)
        return out 
    
    def filter_bat_by_year(self, year):
        data = self._batting
        out = []
        for i in data:
            if int(i['yearID']) >= year:
                out.append(i)
        return out
    
    def compute_aggs_and_year_by_id(self,fields,data=None):
        if data is None:
            data = self._batting
        
        mapped = dict()
        for i in data:
            if not i['playerID'] in mapped:
                values = dict()
                for field_ in fields:
                    values[field_] = float(i[field_])  
                values['first_yr'] = int(i['yearID'])
                values['last_yr'] = int(i['yearID'])
                mapped[i['playerID']] = values
            else:
                ###for each field sum 
                values = mapped[i['playerID']]
                for field_ in fields:
                    values[field_] += float(i[field_])
                if values['first_yr'] > int(i['yearID']):
                    values['first_yr'] = int(i['yearID'])
                if values['last_yr'] < int(i['yearID']):
                    values['last_yr'] = int(i['yearID'])
                mapped[i['playerID']] = values 
 
        return mapped
    
    def compute_batting_avg(self,data):
        for key,val in data.items():
            if val['AB'] ==0:
                val['batting_avg'] = None
            else:
                val['batting_avg'] = val['H']/val['AB']
            data[key] = val
        return data
    
    def filter_AB_by_at_least_value(self,data,ab_filter,yr_filter):
        out = dict()
        for key,val in data.items():
            if(val['AB'] >ab_filter and val['last_yr']>=yr_filter):
                out[key] = val 
        return out
    
    def sort_by_field(self,data,field):
        out = sorted(data.items(), key = lambda x: x[1][field], reverse=True)
        return out
                    
    def join_people(self,data):
        people = self._people
        people_dict = dict()
        for i in people:
            people_dict[i['playerID']] = i
    
        for i in data:
            i[1]['first_name'] = people_dict[i[0]]['nameFirst']
            i[1]['last_name'] = people_dict[i[0]]['nameLast']
        return data
        
'''
d = collections.OrderedDict()

for i in range(0,len(indata)):
    if int(indata[i]['yearID']) >= 1960:
        d[i] = indata[i]
len(d)

from collections import defaultdict, Counter

#dic = defaultdict(Counter)
new_dic = {}
for i in d:
    #print(i) index
    key = d[i]['playerID']
    if key != 'dff1':
        if key not in new_dic: #add player id to new dic
            new_dic[key] = {}
        for k,v in d[i].items(): 
            if k == 'AB':
                if 'total_AB' not in new_dic[key]:
                    new_dic[key]['total_AB'] = float(v)
                else:
                    new_dic[key]['total_AB'] += float(v)
            if k == 'H':
                if 'total_H' not in new_dic[key]:
                    new_dic[key]['total_H'] = float(v)
                else:
                    new_dic[key]['total_H'] += float(v)
                    
                    
subset_dic = {}
for i in new_dic:
    if new_dic[i]['total_AB'] >= 200:
        subset_dic[i] = new_dic[i]
        
        
for i in subset_dic:
    if subset_dic[i]['total_AB'] == 0:
        subset_dic[i]['Batting_Average'] = 0
    else:
        subset_dic[i]['Batting_Average'] = subset_dic[i]['total_H'] / subset_dic[i]['total_AB']
        
sorted_dic = sorted(subset_dic.items(), key = lambda x: x[1]['Batting_Average'], reverse=True)

input_file = csv.DictReader(open("people.csv"))
people = list(input_file)
people[0]


for i in range(0,len(people)):
    key = people[i]['playerID']
    if key in s.keys():
        s[key]['nameFirst'] = people[i]['nameFirst']
        s[key]['nameLast'] = people[i]['nameLast']     
        
# Top Ten
final_dict = {}
count = 0
for i in s:
    if len(final_dict) != 10:
        final_dict[i] = s[i]
        count += 1

# final_d = {}
# for i in 
#     final_d.append(s[i])'''