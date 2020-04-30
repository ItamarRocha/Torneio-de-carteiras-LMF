#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:32:13 2019

@author: itamar
"""
import pandas as pd
import os
import pandas_datareader as web
from datetime import date

data_dir = 'data'

ranking = {
        "Name":[],
        "Monthly":[],
        "Total":[]
        }

data = os.listdir(data_dir)
initial_value = 100000

for filename in data:
    print(filename)
   
    start = filename.split('-',maxsplit = 1)[1].split('.')[0]
    end_day = date.today()
    end = end_day.strftime("%Y-%m-%d")
    
    df = pd.read_csv(data_dir + '/' + filename)
    
    new_df = df.copy()
    
    monthly_initial_value = df['quantities'].sum()
    individual_stocks_appreciation = []
    
    
    df['new_quantities'] = df['quantities']
    
    for stock,percent in zip(df['stocks'], df['quantities']/monthly_initial_value):
        current = web.DataReader(stock + '.SA','yahoo',start,end)['Close']
        stock_appreciation = current.iloc[-1]/current.iloc[0]
        individual_stocks_appreciation.append(stock_appreciation)

    
    df['new_quantities'] = df['quantities']*individual_stocks_appreciation
    
    monthly_appreciation = 0
    
    monthly_appreciation = df['new_quantities'].sum()/df['quantities'].sum() - 1
    
    total_appreciation = 0
    
    total_appreciation = df['new_quantities'].sum()/initial_value - 1
    
    ranking['Name'].append(filename.split('-')[0])
    ranking['Monthly'].append(monthly_appreciation)
    ranking['Total'].append(total_appreciation)
    
    new_df['quantities'] = df['new_quantities']
    
    new_df.to_csv(filename.split('-')[0] + '-' + end + '.csv')
    
final_rank = pd.DataFrame(ranking)