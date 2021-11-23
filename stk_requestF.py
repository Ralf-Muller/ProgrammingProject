


"""Request commands based on the code found in the documentation for Alphavantage/ 
    Link: https://www.alphavantage.co/documentation/"""
"""Validate function by jamylak in stack overflow \
    Link: https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python/16870699"""
"""Some other references for pandas operations from pandas documentation \
    Link: https://pandas.pydata.org/docs/reference/frame.html"""



import requests
import pandas as pd
from datetime import datetime
import tkinter as tk

#def validate(date_text):   
    #From jamylak
    #Validates the date format
 #   try:
  #      datetime.strptime(date_text, '%Y-%m-%d')
   # except ValueError:
    #    raise ValueError("Incorrect data format, should be YYYY-MM-DD")
def validate(start_date, end_date):   
        #From jamylak
        #Validates the date format
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise tk.messagebox.showerror("Error", "Incorrect date format. Please use YYYY-MM-DD.")
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise tk.messagebox.showerror("Error", "Incorrect date format. Please use YYYY-MM-DD.")
            
            
def date_order(start_date, end_date):
        #Checks if the date range is valid
    if end_date <= start_date:
        raise tk.messagebox.showerror("Error", "Invalid date range. Please try again")

def date_slicer(stk_frame, stock_dict, stock, start_date, end_date):
    #Returns:
    #1. The Stock dictionary updated with the dataframe
    #It also produces a csv file per stock with the data
    try:
        date_frame = pd.DataFrame(stk_frame["Time Series (Daily)"], dtype = "float").T.sort_index()
    except KeyError:
        raise tk.messagebox.showerror("Error", "Stock not found. Did you use the correct symbol? Please try again")
    sliced_frame = date_frame.loc[start_date:end_date]
    stock_dict[stock] = sliced_frame
    #sliced_frame.to_csv("{} Data From {} to {}".format(stock, start_date, end_date))
    return stock_dict

def stock_exists(stock, key):
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}'.format(\
                                                  stock, key)
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
        raise tk.messagebox.showerror("Error", "Stock not found. Please use Request Symbol Function to find correct stock") 
    stock_dict[stock] = 0  
    url = 'https://www.alphavantage.co/query?function={}&symbol={}&outputsize=full&apikey={}'.format(\
                                                  funct, stock, key)
    req_stk = requests.get(url)
    stk_frame = req_stk.json()
    stock_dict = date_slicer(stk_frame, stock_dict, stock, start_date, end_date)
    return stock_dict
    
    
def req_to_frame(stock_dict, key, stock, start_date, end_date):
    #Putting all together
    stock_dict = stock_query(stock_dict, key, stock, start_date, end_date)
    return stock_dict    


#<<<<<<< HEAD
#def main():
 #   key = input("Please feed me your key for Alphavantage : ")
  #  stock = input("Please feed me a company's stock name : ")
   # start_date = input("Please feed me the starting date in YYYY-MM-DD format: ")
   # end_date = input("Please feed me the ending date in YYYY-MM-DD format: ")
   # s_dict = req_to_frame(key, stock, start_date, end_date)

#if __name__ == "__main__":
 #   main()

#<<<<<<< HEAD
#key = input("Please feed me your key for Alphavantage : ")
#stock = input("Please feed me a company's stock name : ")
#start_date = input("Please feed me the starting date in YYYY-MM-DD format: ")
#end_date = input("Please feed me the ending date in YYYY-MM-DD format: ")
#s_dict = req_to_frame(key, stock, start_date, end_date)



#=======
#key = input("Please feed me your key for Alphavantage : ")
#if key == '':
    #raise Exception('Please enter a correct API Key')
#stock = input("Please feed me a company's stock name : ")
#if stock_exists(stock, key) == False:
 #   raise Exception("Stock not found. Please use Request Symbol Function to find correct stock")
#start_date = input("Please feed me the starting date in YYYY-MM-DD format: ")
#end_date = input("Please feed me the ending date in YYYY-MM-DD format: ")
#stock_dict = req_to_frame(key, stock, start_date, end_date)
#>>>>>>> 45359415ff0f027b20b4bc102674104b3bb50c58
#>>>>>>> bf7499abf1727dda6d8ade832874c6a3817c4356

