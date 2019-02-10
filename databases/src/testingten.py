# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:22:06 2019

@author: James
"""
from TenGreatestHitters import TenGreatestHitters

x = TenGreatestHitters()
out2 = x.compute_aggs_and_year_by_id(['AB','H'])
out3 = x.compute_batting_avg(out2)
out4 = x.filter_AB_by_at_least_value(out3,200,1960)
out5 = x.sort_by_field(out4,'batting_avg')
out6 = x.join_people(out5)
print()
for idx,i in enumerate(out6):
    print('{} {} {}'.format(i[0], i[1]['batting_avg'],i[1]['first_name']))
    if idx ==9:
        break