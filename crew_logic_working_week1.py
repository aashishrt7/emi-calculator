# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:47:41 2023

@author: Aashish
"""

import pandas as pd
import os
import platform
from datetime import datetime, date, timedelta

#%% 
rest_out_long = 480
rest_out_short = 360
rest_home = 960
home_stn = 1

#%%
weeks = 1 #no. of weeks
days = ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']

def convert_min(time, week, day):
    day_num = days.index(day)
    return time + week*1440*7 + day_num*1440
    
#%% 
raw_data = pd.read_csv("C:/Users/Aashish/Downloads/MumbaiDiv-TT v2 - Non Sr. staff data-2.csv")
raw_data = raw_data.set_index('task')

#%%
data_3d = [raw_data]*weeks
weekwise_category = [0]*weeks
categories = []
#%% 
for week_num in range(weeks):
    data = data_3d[week_num]
    data['sign_on'] = data.apply(lambda row: convert_min(row['sign_on'], 0, row['day']), axis = 1)
    data['sign_off'] = data.apply(lambda row: convert_min(row['sign_off'], 0, row['day']), axis = 1)
    
    #%% 
    data = data.sort_values(['sign_on', 'task'], ascending = [True, True])
    data['category'] = -1
    
    #%% 
    for i,row in data.iterrows():
        min_quantity = 1000000
        min_workload = 1000000
        workloads = data.groupby('category').sum()['sign_off'] - data.groupby('category').sum()['sign_on']
        for j in range(len(categories)):
            cnt_ndh = -1 
            tasks = categories[j]
            
            if data.loc[tasks[-1], 'dest_code'] != row['org_code']:
                continue
            try:
                workload = workloads[j]
            except:
                workload = 0
    
            if len(tasks)>=4:
                cnt_ndh = data.loc[tasks[-4:], 'ndh_flag'].sum() + row['ndh_flag']
            if cnt_ndh >= 5: 
                continue
            #print("reached here")
            
            traversal_time = data.loc[tasks[-1], 'sign_off'] - data.loc[tasks[-1], 'sign_on']
            rest_time = row['sign_on'] - data.loc[tasks[-1], 'sign_off']
            
            curr_trip_time = row['sign_off']  - row['sign_on'] 
            if workload + curr_trip_time >= 52*60:
                continue
            
            if row['org_code'] != home_stn:
                #print("reached_here:1")
                if traversal_time>480 and rest_time > rest_out_long:
                    if data.loc[tasks[-1], 'sign_off'] + rest_out_long <min_quantity:
                        data.loc[i, 'category'] = j
                        min_quantity = data.loc[tasks[-1], 'sign_off'] + rest_out_long
                        min_workload = workload
                    elif (data.loc[tasks[-1], 'sign_off'] + rest_out_long == min_quantity) and workload<min_workload:
                        data.loc[i, 'category'] = j
                        min_workload = workload
                elif traversal_time <=480 and rest_time > rest_out_short:
                    if data.loc[tasks[-1], 'sign_off'] + rest_out_short <min_quantity:
                        data.loc[i, 'category'] = j
                        min_quantity = data.loc[tasks[-1], 'sign_off'] + rest_out_short
                        min_workload = workload
                    elif (data.loc[tasks[-1], 'sign_off'] + rest_out_short == min_quantity) and workload<min_workload:
                        data.loc[i, 'category'] = j
                        min_workload = workload
            elif row['org_code'] == home_stn and rest_time > rest_home:
                if workload < min_workload:
                    data.loc[i, 'category'] = j
                    min_quantity = data.loc[tasks[-1], 'sign_off'] + rest_home
                    min_workload = workload
                elif workload == min_workload and data.loc[tasks[-1], 'sign_off'] + rest_home <min_quantity:
                    data.loc[i, 'category'] = j
                    min_quantity = data.loc[tasks[-1], 'sign_off'] + rest_home
                    
        if data.loc[i, 'category']>=0:
            categories[data.loc[i, 'category']].append(i)
        else:
            categories.append([i])
            data.loc[i, 'category'] = len(categories) -1
    
    weekwise_category[i] = [len(x) for x in categories]
  
#%%

    


