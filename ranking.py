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
import numpy as np
import sys

data_dir = 'newformat_data'

ranking = {
        "Name":[],
        "Monthly":[],
        "Total":[]
        }

today = date.today()
today = today.strftime("%Y-%m-%d")
month_init = '2020-04-30'#sys.argv[1]#'2020-' + today.split('-')[1] + '-01'

for file in os.listdir(data_dir):
    
    df = pd.read_excel(f'{data_dir}/{file}')
    
    df.columns = [int(column.split(': ')[1]) for column in df.columns]
    df = df.fillna(value = 0)
    print(file)
    
    stocks = []
    #composition = []
    buy_prices = []
    montante = []
    
    for i in range(10):
        stocks.append(df.iloc[6+i, 3])
        #composition.append(df.iloc[6+i, 4])
        buy_prices.append(df.iloc[6+i, 5])
        montante.append(df.iloc[6+i, 8])
        
    month_initial_value = df.iloc[2, 3]
    
    todays_price = []
    #buy_prices = []
    
    j=0
    for stock in stocks:
        
        try:
            closing_prices = web.DataReader(stock + '.SA','yahoo',month_init,today)['Close']
            todays_price.append(closing_prices[-1]) #pega apenas a ultima cotação
            if '11' not in stock:
                buy_prices[j] = (closing_prices[0]) #pega o preço de compra
            print(f"{stock} -> buy : {buy_prices[j]}, end : {closing_prices[-1]}")
        except:
            todays_price.append(0)
            print(f'{stock} not recognized')
        j+=1
        
    stocks_monthly_appreciation = [(today/buy) for buy,today in zip(buy_prices,todays_price) if buy != 0]
    stocks_current_mont = [(mont * appreciation) for mont,appreciation in zip(montante,stocks_monthly_appreciation)]
    
    current_value = sum(stocks_current_mont) + (month_initial_value - sum(montante)) #adiciona o caixa tmb
    
    monthly_appreciation = (current_value/month_initial_value - 1)*100
    total_appreciation = (current_value/100000 - 1) * 100
    
    ranking['Name'].append(file.split('.')[0].split('_-_')[1])
    ranking['Monthly'].append(monthly_appreciation)
    ranking['Total'].append(total_appreciation)
    
final_rank = pd.DataFrame(ranking)

print(final_rank.sort_values(by='Monthly'))