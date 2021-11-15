
#References

"""Request commands based on the code found in the documentation for Alphavantage/ 
    Link: https://www.alphavantage.co/documentation/"""
"""Validate function by jamylak in stack overflow \
    Link: https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python/16870699"""
"""Some other references for pandas operations from pandas documentation \
    Link: https://pandas.pydata.org/docs/reference/frame.html"""

#HOW TO USE:
    #STEP 1: Get your alphavantage key
    #STEP 2: Look for a company symbol using symb_names()
    #Step 3: Return req_to_frame to obtain a dictionary. Assign it to a variable
    #Examples on line 109 and 110



#key: 7QJ0OD6RU5IEVRO4

import requests
import pandas as pd
import datetime

def req_list_symb():
    #Function that asks the user to input their key and a name
    #Returns a dictionary with a list of the companies 
    #with the most similar name
    key = input("Please feed me your key for Alphavantage : ")
    symbol_func = "SYMBOL_SEARCH"
    keywords = input("Tell me the company name: ")
    symbol_url = 'https://www.alphavantage.co/query?function={}&keywords={}&apikey={}'.format(
    symbol_func, keywords, key)
    req_symb = requests.get(symbol_url)
    comp_stock = req_symb.json()
    return comp_stock, key


def comp_list(comp_stock):
    #Prints out the search results for the company symbols request
    if len(comp_stock['bestMatches']) > 0:
        for company in comp_stock['bestMatches']:
            print("Company Symbol : ", company['1. symbol'], "\n",  
              "Company Name : ", company['2. name'], "\n",
              "Stock Type : ", company['3. type'], "\n", 
              "Region : ", company['4. region'], "\n")
        print("If you want to look for a stock info, please use the company symbol")
    else:
        print("No companies were found. Try again")
    

def symb_names():
    #Looking up a company's symbol
    comp_stock = req_list_symb()
    comp_list(comp_stock)
    
def validate(date_text):   
    #From jamylak
    #Validates the date format
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        
def date_order(start_date, end_date):
    #Checks if the date range is valid
    if end_date <= start_date:
        raise Exception("Invalid date range. Please try again")

def date_slicer(stk_frame, stock_dict, stock, start_date, end_date):
    #Returns:
    #1. The Stock dictionary updated with the dataframe
    #It also produces a csv file per stock with the data
    try:
        date_frame = pd.DataFrame(stk_frame["Time Series (Daily)"], dtype = "float").T.sort_index()
    except KeyError:
        raise KeyError("Stock not found. Did you use the correct symbol? Please try again")
    sliced_frame = date_frame.loc[start_date:end_date]
    stock_dict[stock] = sliced_frame
    sliced_frame.to_csv("{} Data From {} to {}".format(stock, start_date, end_date))
    return stock_dict

def get_description(stock, key, start_date, end_date):
    import numpy as np
    import statistics
    from operator import itemgetter
    import json
    
    url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'.format(stock, key)
    r = requests.get(url)
    info = r.json()
    
    print('--'*50, '\nCompany overview:')
    overview = pd.DataFrame(itemgetter('Symbol', 'Name', 'Country', 'Sector', 'Industry')(info), 
    index = ['Symbol:', 'Name:', 'Country:', 'Sector:', 'Industry:'])
    print(overview)

    data = pd.read_csv('{} Data From {} to {}'.format(stock, start_date, end_date))
    closing = data.loc[:,'5. adjusted close']

    print('\nAdjusted closing price of selected company from {} to {}:'.format(start_date, end_date))
    print(' Mean               : ', "%.2f" % np.mean(closing), '\n', 
          'Median             : ', "%.2f" % np.median(closing), '\n', 
          'Standard deviation : ', "%.2f" % statistics.stdev(closing), '\n',
          'Variance           : ', "%.2f" % statistics.variance(closing), '\n',
          'Range              : from', "%.2f" % min(closing), 'to', "%.2f" % max(closing), '\n',
          'Q1 Quartiles       : ', "%.2f" % np.quantile(closing, .25, interpolation='midpoint'), '\n',
          'Q2 Quartiles       : ', "%.2f" % np.quantile(closing, .50, interpolation='midpoint'), '\n',
          'Q3 Quartiles       : ', "%.2f" % np.quantile(closing, .75, interpolation='midpoint'), '\n',
          )

def stock_query():
    #Asks the user for a key, date range, and stock 
    #and returns a dictionary with all the requested stocks
    stock_dict = {}

    
    key = input("Please feed me your key for Alphavantage : ")
    stock = input("Please feed me a company's stock name : ")
    start_date = input("Please feed me the starting date in YYYY-MM-DD format: ")
    validate(start_date)
    end_date = input("Please feed me the ending date in YYYY-MM-DD format: ")
    validate(end_date)
    date_order(start_date, end_date)
    funct = "TIME_SERIES_DAILY_ADJUSTED"
    while stock != "0" :
        stock_dict[stock] = 0  
        url = 'https://www.alphavantage.co/query?function={}&symbol={}&outputsize=full&apikey={}'.format(\
                                                  funct, stock, key)
        req_stk = requests.get(url)
        stk_frame = req_stk.json()
        stock_dict = date_slicer(stk_frame, stock_dict, stock, start_date, end_date)

        #get the overview
        get_description(stock, key, start_date, end_date)
        stock = input("Please feed me a company's stock name or 0 to quit: ")
    return stock_dict
    

    
def req_to_frame():
    #Putting all together
    stock_dict = stock_query()
    return stock_dict    

#symb_names()  
stock_dict = req_to_frame()