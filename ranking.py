
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

data_dir = 'Junho'

units = {'BPAC11':48.84,'KLBN11':19.56,'SAPR11':27.60,'TAEE11':28.75	,
         'TIET11':13.73}

stocks_dict = {}

ranking = {
        "Name":[],
        "Monthly":[],
        "Total":[]
        }

today = date.today()
today = today.strftime("%Y-%m-%d")
month_init = '2020-05-29'#sys.argv[1]#'2020-' + today.split('-')[1] + '-01'

for file in os.listdir(data_dir):
    
    xls = pd.ExcelFile(f'{data_dir}/{file}')
    
    df = pd.read_excel(xls,data_dir)
    
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
        print(df.iloc[6+i, 5])
        
    month_initial_value = df.iloc[2, 3]
    
    todays_price = []
    #buy_prices = []
    
    j=0
    for stock in stocks:
        try:
            stock = stock.strip() #remove white spaces
            if stock not in stocks_dict:
                closing_prices = web.DataReader(stock + '.SA','yahoo',month_init,today)['Close']
                todays_price.append(closing_prices[-1]) #pega apenas a ultima cotação
                stocks_dict[stock] = closing_prices
            else:
                todays_price.append(stocks_dict[stock][-1])
                
            if '11' not in stock:
                buy_prices[j] = (stocks_dict[stock][0]) #pega o preço de compra
            elif stock in units:
                buy_prices[j] = units[stock]
            print(f"{stock} -> buy : {buy_prices[j]}, end : {stocks_dict[stock][-1]}")
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

relation_open_close = pd.DataFrame()
for stock in stocks_dict:
    relation_open_close[stock] = pd.Series([stocks_dict[stock][0],stocks_dict[stock][-1]])
    
relation_open_close = relation_open_close.T
relation_open_close.to_csv("cotacoes.csv")
final_rank.to_csv("rank_final.csv")