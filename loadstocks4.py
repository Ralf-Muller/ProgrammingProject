
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 17:29:36 2021

@author: Rachel
"""

#key: 7QJ0OD6RU5IEVRO4

import tkinter as tk
import requests
import pandas as pd
import datetime

class ChooseStock:
    def __init__(self, master):
        self.master = master

        master.title("Stock Analyser")

        self.greet = tk.Label(master, text="Welcome to the Stocks Analyser.")
        self.greet.pack(pady=10)

        self.find = tk.Button(master, text="Find Company Symbol", command = self.symb_names)
        self.find.pack(pady=10)
        self.enter = tk.Button(master, text="Enter Company Symbol", command = self.req_to_frame)
        self.enter.pack(pady=10)
        
    def symb_names(self):
        #Looking up a company's symbol
        comp_stock = self.req_list_symb()
        return comp_stock
    
    def req_list_symb(self):
        #Function that asks the user to input their key and a name
        #Returns a dictionary with a list of the companies 
        #with the most similar name
        key_q = tk.Label(text="Please enter Alphavantage key: ")
        key = tk.Entry()
        key_q.pack()
        key.pack()
        key = key.get()
             
        keywords_q = tk.Label(text="Please enter company name: ")
        keywords = tk.Entry()
        keywords_q.pack()
        keywords.pack()
        keywords = keywords.get()
        
        symbol_func = "SYMBOL_SEARCH"
        
        symbol_url = 'https://www.alphavantage.co/query?function={}&keywords={}&apikey={}'.format(
            symbol_func, keywords, key)
        req_symb = requests.get(symbol_url)
        comp_stock = req_symb.json()
        search = tk.Button(text="Search", command = lambda: self.comp_list(comp_stock))
        search.pack(pady=10)
    
    def comp_list(self, comp_stock):
    #Prints out the search results for the company symbols request
        if len(comp_stock['bestMatches']) > 0:
            for company in comp_stock['bestMatches']:
                self.msg_window("Company Symbol : " + company['1. symbol'] + "\n" +  
                            "Company Name : " + company['2. name'] + "\n" +
                            "Stock Type : " + company['3. type'] + "\n" +
                            "Region : " + company['4. region'] + "\n")
        else:
            self.msg_window("No companies were found. Try again")
    
    def req_to_frame(self):
        #Putting all together
        stock_dict = self.stock_query()
        return stock_dict
    
    def stock_query(self):
        #Asks the user for a key, date range, and stock 
        #and returns a dictionary with all the requested stocks
        stock_dict = {}
        
        key_q = tk.Label(text = "Please enter Alphavantage key : ")
        key = tk.Entry()
        key_q.pack()
        key.pack()
        key = key.get()
        
        stock_q = tk.Label(text="Please enter company symbol: ")
        stock = tk.Entry()
        stock_q.pack()
        stock.pack()
        stock = stock.get()
        
        start_date_q = tk.Label(text = "Please enter start date in YYYY-MM-DD format: ")
        start_date = tk.Entry()
        start_date_q.pack()
        start_date.pack()
        start_date = start_date.get()
        
        enddate_q = tk.Label(text = "Please enter end date in YYYY-MM-DD format: ")
        end_date = tk.Entry()
        enddate_q.pack()
        end_date.pack(pady=10)
        end_date = end_date.get()

        funct = "TIME_SERIES_DAILY_ADJUSTED"
        stock_dict[stock] = 0  
        url = 'https://www.alphavantage.co/query?function={}&symbol={}&outputsize=full&apikey={}'.format(\
                                                      funct, stock, key)
        req_stk = requests.get(url)
        stk_frame = req_stk.json()
        
        getdata = tk.Button(text = "Get Data", command = lambda: self.date_slicer(stk_frame, stock_dict, stock, start_date, end_date))
        getdata.pack(pady=10)
        
        exit = tk.Button(text = "Quit", command = self.quit)
        exit.pack(pady=10)
    
    def date_slicer(self, stk_frame, stock_dict, stock, start_date, end_date):
        #Returns:
        #1. The Stock dictionary updated with the dataframe
        #It also produces a csv file per stock with the dat
        try:
            date_frame = pd.DataFrame(stk_frame["Time Series (Daily)"], dtype = "Float").T.sort_index()
        except KeyError:
            tk.messagebox.showinfo("Error", "Stocks not found. Did you use the correct symbol? Please try again.")
        sliced_frame = date_frame.loc[start_date:end_date]
        self.stock_dict[stock] = sliced_frame
        sliced_frame.to_csv("{} Data From {} to {}".format(stock, start_date, end_date))
        self.msg_window("Your stock information has been retrieved.")
        
    def msg_window(self, msg):
        #Create message window
        child = tk.Toplevel(self.master)
        label = tk.Label(child, text = msg)
        label.pack()
    
    def quit(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    ChooseStock(root)
    root.mainloop()