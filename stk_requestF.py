"""Request commands based on the code in the documentation for Alphavantage/ 
Link: https://www.alphavantage.co/documentation/
Validate function by jamylak in stack overflow : 
https://stackoverflow.com/questions/16870663/\
how-do-i-validate-a-date-string-format-in-python/16870699
Some other references for pandas operations from pandas documentation \
Link: https://pandas.pydata.org/docs/reference/frame.html"""


import requests
import pandas as pd
from datetime import datetime
import tkinter as tk


def validate(start_date, end_date):   
        #From jamylak
        #Validates the date format
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise tk.messagebox.showerror("Error", 
                              "Incorrect date format. Please use YYYY-MM-DD.")
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise tk.messagebox.showerror("Error", 
                              "Incorrect date format. Please use YYYY-MM-DD.")
            
            
def date_order(start_date, end_date):
        #Checks if the date range is valid
    if end_date <= start_date:
        raise tk.messagebox.showerror("Error", 
                              "Invalid date range. Please try again")


def date_slicer(stk_frame, stock_dict, stock, start_date, end_date):
    #Returns:
    #1. The Stock dictionary updated with the dataframe
    try:
        date_frame = pd.DataFrame(stk_frame["Time Series (Daily)"],
                                            dtype = "float").T.sort_index()
    except KeyError:
        raise tk.messagebox.showerror("Error", 
          "Stock not found. Did you use the correct symbol? Please try again")
    sliced_frame = date_frame.loc[start_date:end_date]
    stock_dict[stock] = sliced_frame
    return stock_dict


def stock_exists(stock, key):
    #Function for checking that the stock exists
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}'.format(stock, key)
    req_stk = requests.get(url)
    stk_frame = req_stk.json()
    best_matches = stk_frame['bestMatches']
    for company in best_matches:
        if stock == company["1. symbol"]:
            return True
    return False


def stock_query(stock_dict, key, stock, start_date, end_date):
    #Asks the user for a key, date range, and stock 
    #and returns a dictionary with all the requested stocks
    if key == '':
        raise tk.messagebox.showerror("Error",'Please enter a correct API Key')
    validate(start_date, end_date)
    date_order(start_date, end_date)
    funct = "TIME_SERIES_DAILY_ADJUSTED"
    if stock_exists(stock, key) == False:
        raise tk.messagebox.showerror("Error", 
          "Stock not found. Please use Find Symbol Function to find correct stock") 
    stock_dict[stock] = 0  
    url = 'https://www.alphavantage.co/query?function={}&symbol={}&outputsize=full&apikey={}'.format(funct, stock, key)
    req_stk = requests.get(url)
    stk_frame = req_stk.json()
    stock_dict = date_slicer(stk_frame, stock_dict, stock, start_date,
                             end_date)
    return stock_dict
    
    
def req_to_frame(stock_dict, key, stock, start_date, end_date):
    #Putting all together
    stock_dict = stock_query(stock_dict, key, stock, start_date, end_date)
    return stock_dict    



