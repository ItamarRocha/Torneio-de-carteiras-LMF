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

def preprocess_excel(df):
    
    
    return df

data_dir = 'newformat_data'

ranking = {
        "Name":[],
        "Monthly":[],
        "Total":[]
        }

data = os.listdir(data_dir)
initial_value = 100000


df = pd.read_excel(f'{data_dir}/05_Maio_-_Igor_Simões.xlsx')

df.columns = [int(column.split(': ')[1]) for column in df.columns]
