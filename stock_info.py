import stk_requestF as sr
import requests
import pandas as pd
import numpy as np
import statistics
from operator import itemgetter
import json


#key: 7QJ0OD6RU5IEVRO4


def get_overview(stock, key):

    url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'.format(stock, key)
    r = requests.get(url)
    info = r.json()
    
    print('--'*50, '\nCompany overview:')
    overview = pd.DataFrame(itemgetter('Symbol', 'Name', 'Country', 'Sector', 'Industry')(info), 
    index = ['Symbol:', 'Name:', 'Country:', 'Sector:', 'Industry:'])
    print(overview)



def get_description(s_dict, stock):

    values = s_dict[stock]['5. adjusted close']
    #data = pd.read_csv('{} Data From {} to {}'.format(stock, start_date, end_date))

    print('\nAdjusted closing price of {} from {} to {}:'.format(stock, values.index[0], values.index[-1]))
    print(' Mean               : ', "%.2f" % np.mean(values), '\n', 
          'Median             : ', "%.2f" % np.median(values), '\n', 
          'Standard deviation : ', "%.2f" % statistics.stdev(values), '\n',
          'Variance           : ', "%.2f" % statistics.variance(values), '\n',
          'Range              : from', "%.2f" % min(values), 'to', "%.2f" % max(values), '\n',
          'Q1 Quartiles       : ', "%.2f" % np.quantile(values, .25, interpolation='midpoint'), '\n',
          'Q2 Quartiles       : ', "%.2f" % np.quantile(values, .50, interpolation='midpoint'), '\n',
          'Q3 Quartiles       : ', "%.2f" % np.quantile(values, .75, interpolation='midpoint'), '\n',
          )


#key = input("Please feed me your key for Alphavantage : ")
#stock = input("Please feed me a company's stock name : ")
#start_date = input("Please feed me the starting date in YYYY-MM-DD format: ")
#end_date = input("Please feed me the ending date in YYYY-MM-DD format: ")
s_dict = sr.req_to_frame(key, stock, start_date, end_date)

get_overview(stock, key)
get_description(s_dict, stock)