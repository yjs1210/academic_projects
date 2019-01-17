\* Let's cut some rolls *\
Minimize
min: five_42cms + four_42cms + one_108cm + one_108cm_four_42cms
 + one_108cm_one_42cm + one_108cm_one_93cm + one_108cm_one_93cm_one_42cm
 + one_108cm_one_93cm_two_42cms + one_108cm_three_42cms + one_108cm_two_42cms
 + one_108cm_two_93cms + one_135cm + one_135cm_one_108cm
 + one_135cm_one_108cm_one_42cm + one_135cm_one_42cm + one_135cm_one_93cm
 + one_135cm_one_93cm_one_42cm + one_135cm_three_42cms + one_135cm_two_42cms
 + one_42cm + one_93cm + one_93cm_four_42_cms + one_93cm_one_42cm
 + one_93cm_three_42cms + one_93cm_two_42cms + seven_42cms + six_42cms
 + three_42cms + three_93cms + two_108cm + two_108cms_one_42cm
 + two_108cms_two_42cms + two_135cms + two_42cms + two_93cms
 + two_93cms_one_42cm + two_93cms_two_42cms
Subject To
Roll_1_Demand: one_135cm + one_135cm_one_108cm + one_135cm_one_108cm_one_42cm
 + one_135cm_one_42cm + one_135cm_one_93cm + one_135cm_one_93cm_one_42cm
 + one_135cm_three_42cms + one_135cm_two_42cms + 2 two_135cms = 97
Roll_2_Demand: one_108cm + one_108cm_four_42cms + one_108cm_one_42cm
 + one_108cm_one_93cm + one_108cm_one_93cm_one_42cm
 + one_108cm_one_93cm_two_42cms + one_108cm_three_42cms + one_108cm_two_42cms
 + one_108cm_two_93cms + one_135cm_one_108cm + one_135cm_one_108cm_one_42cm
 + seven_42cms + 2 two_108cm + 2 two_108cms_one_42cm + 2 two_108cms_two_42cms
 = 610
Roll_3_Demand: one_108cm_one_93cm + one_108cm_one_93cm_one_42cm
 + one_108cm_one_93cm_two_42cms + 2 one_108cm_two_93cms + one_135cm_one_93cm
 + one_135cm_one_93cm_one_42cm + one_93cm + one_93cm_four_42_cms
 + one_93cm_one_42cm + one_93cm_three_42cms + one_93cm_two_42cms
 + 3 three_93cms + 2 two_93cms + 2 two_93cms_one_42cm + 2 two_93cms_two_42cms
 = 305
Roll_4_Demand: 5 five_42cms + 4 four_42cms + 4 one_108cm_four_42cms
 + one_108cm_one_42cm + one_108cm_one_93cm_one_42cm
 + 2 one_108cm_one_93cm_two_42cms + 3 one_108cm_three_42cms
 + 2 one_108cm_two_42cms + one_135cm_one_108cm_one_42cm + one_135cm_one_42cm
 + one_135cm_one_93cm_one_42cm + 3 one_135cm_three_42cms
 + 2 one_135cm_two_42cms + one_42cm + 4 one_93cm_four_42_cms
 + one_93cm_one_42cm + 3 one_93cm_three_42cms + 2 one_93cm_two_42cms
 + 7 seven_42cms + 6 six_42cms + 3 three_42cms + two_108cms_one_42cm
 + 2 two_108cms_two_42cms + 2 two_42cms + two_93cms_one_42cm
 + 2 two_93cms_two_42cms = 211
Bounds
0 <= five_42cms
0 <= four_42cms
0 <= one_108cm
0 <= one_108cm_four_42cms
0 <= one_108cm_one_42cm
0 <= one_108cm_one_93cm
0 <= one_108cm_one_93cm_one_42cm
0 <= one_108cm_one_93cm_two_42cms
0 <= one_108cm_three_42cms
0 <= one_108cm_two_42cms
0 <= one_108cm_two_93cms
0 <= one_135cm
0 <= one_135cm_one_108cm
0 <= one_135cm_one_108cm_one_42cm
0 <= one_135cm_one_42cm
0 <= one_135cm_one_93cm
0 <= one_135cm_one_93cm_one_42cm
0 <= one_135cm_three_42cms
0 <= one_135cm_two_42cms
0 <= one_42cm
0 <= one_93cm
0 <= one_93cm_four_42_cms
0 <= one_93cm_one_42cm
0 <= one_93cm_three_42cms
0 <= one_93cm_two_42cms
0 <= seven_42cms
0 <= six_42cms
0 <= three_42cms
0 <= three_93cms
0 <= two_108cm
0 <= two_108cms_one_42cm
0 <= two_108cms_two_42cms
0 <= two_135cms
0 <= two_42cms
0 <= two_93cms
0 <= two_93cms_one_42cm
0 <= two_93cms_two_42cms
Generals
five_42cms
four_42cms
one_108cm
one_108cm_four_42cms
one_108cm_one_42cm
one_108cm_one_93cm
one_108cm_one_93cm_one_42cm
one_108cm_one_93cm_two_42cms
one_108cm_three_42cms
one_108cm_two_42cms
one_108cm_two_93cms
one_135cm
one_135cm_one_108cm
one_135cm_one_108cm_one_42cm
one_135cm_one_42cm
one_135cm_one_93cm
one_135cm_one_93cm_one_42cm
one_135cm_three_42cms
one_135cm_two_42cms
one_42cm
one_93cm
one_93cm_four_42_cms
one_93cm_one_42cm
one_93cm_three_42cms
one_93cm_two_42cms
seven_42cms
six_42cms
three_42cms
three_93cms
two_108cm
two_108cms_one_42cm
two_108cms_two_42cms
two_135cms
two_42cms
two_93cms
two_93cms_one_42cm
two_93cms_two_42cms
End
