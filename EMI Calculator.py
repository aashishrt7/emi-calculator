# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 09:17:39 2022

@author: aashish
"""

print("\n*** EMI Calculator ***\n")
import pandas as pd
df = pd.DataFrame({"symbol": ['d', 'w', 'm', 'y'],
                  "factor": [365, 52, 12, 1],
                  "name": ['days', "weeks", "months", "years"]})
df.set_index('symbol', inplace = True)
P = float(input("Principal Amount: "))
tu = input("Choose time units: (d -> days; w -> weeks; m -> months; y -> years)\n")
n = int(input(f"time (in {df.loc[tu, 'name']}): "))
rpa = float(input("rate of interest (p.a.): "))
r = 0.01*rpa/float(df.loc[tu, 'factor'])
E = int(P * (r * (1+r)**n)/((1+r)**n - 1))
s = u"\u20B9"
print(f"EMI : {s}{E} per {df.loc[tu, 'name']}")
print("\n*** End ***\n")



