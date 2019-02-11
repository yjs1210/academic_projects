# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 14:10:10 2019

@author: James
"""

import csv as csv

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
    
if __name__ == '__main__':
    x = TenGreatestHitters()
    out2 = x.compute_aggs_and_year_by_id(['AB','H'])
    out3 = x.compute_batting_avg(out2)
    out4 = x.filter_AB_by_at_least_value(out3,200,1960)
    out5 = x.sort_by_field(out4,'batting_avg')
    out6 = x.join_people(out5)
    for idx,i in enumerate(out6):
        print('{} {} {}'.format(i[0], i[1]['batting_avg'],i[1]['first_name']))
        if idx ==9:
            break
    