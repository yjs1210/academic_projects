\* The Miracle Worker *\
Minimize
Health_restored;_to_be_maximized: cut_typ_1 + cut_typ_2
Subject To
Herb_A_constraint: 3 cut_typ_1 + 4 cut_typ_2 <= 25
Herb_B_constraint: 2 cut_typ_1 + cut_typ_2 <= 10
Bounds
0 <= cut_typ_1
0 <= cut_typ_2
Generals
cut_typ_1
cut_typ_2
End
