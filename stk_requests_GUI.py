# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 15:23:24 2021

@author: Rachel
"""

import tkinter as tk
import requests
import numpy as np
import pandas as pd
import datetime

s_dict = {}

class ChooseStock:
    def __init__(self, master):
        self.master = master

        master.title("Stock Analyser")
        
        self.heading_font = ("Lato", 12, "bold")
        self.button_font = ("Lato", 11)
        self.text_font = ("Lato", 11)
        self.heading_2_font = ("Lato", 11, "bold")
        
        self.greet = tk.Label(master, text="Welcome to the Stocks Analyser.", font = self.heading_font )
        self.greet.pack(pady=10, padx=10)

        self.find = tk.Button(width = 20, text="Find Company Symbol", font = self.button_font, command = self.find_symbol)
        self.find.pack(pady=10, padx=10)
        self.enter = tk.Button(width = 20, text="Enter Company Symbol", font = self.button_font, command = self.enter_symbol)
        self.enter.pack(pady=10, padx=10)
        exit = tk.Button(text="Quit", width = 20, font = self.button_font, command = self.quit)
        exit.pack(pady = 10, padx=10)
    
    def find_symbol(self):
        # Inputs to find symbol
        child = tk.Toplevel(self.master)
        self.greet = tk.Label(child, text = "Please enter details to find a company symbol: ", font = self.heading_2_font)
        self.greet.pack(pady=10, padx=10)
        
        key_q = tk.Label(child,text="Please enter Alphavantage key: ", font = self.text_font)
        self.key = tk.Entry(child,font = self.text_font)
        key_q.pack(pady=5, padx=5)
        self.key.pack(pady=5, padx=5)
             
        keywords_q = tk.Label(child,text="Please enter company name: ", font = self.text_font)
        self.keywords = tk.Entry(child,font = self.text_font)
        keywords_q.pack(pady=5, padx=5)
        self.keywords.pack(pady=5, padx=5)
        
        find = tk.Button(child,text="Search", width = 10, font = self.button_font, command = lambda: self.symb_names(self.keywords.get(), self.key.get()))
        find.pack(pady=10, padx=10)
        
    def enter_symbol(self):
        # Inputs to enter symbol
        child = tk.Toplevel(self.master)
        self.greet = tk.Label(child, text = "Please enter details to load stock information: ", font = self.heading_2_font)
        self.greet.pack(pady=10, padx=10)

        key_q = tk.Label(child,text = "Please enter Alphavantage key: ", font = self.text_font)
        self.key = tk.Entry(child,font = self.text_font)
        key_q.pack(pady=5, padx=5)
        self.key.pack(pady=5, padx=5)
        
        stock_q = tk.Label(child,text="Please enter company symbol: ", font = self.text_font)
        self.stock = tk.Entry(child,font = self.text_font)
        stock_q.pack(pady=5, padx=5)
        self.stock.pack(pady=5, padx=5)
        
        start_date_q = tk.Label(child,text = "Please enter start date in YYYY-MM-DD format: ", font = self.text_font)
        self.start_date = tk.Entry(child,font = self.text_font)
        start_date_q.pack(pady=5, padx=5)
        self.start_date.pack(pady=5, padx=5)
        
        enddate_q = tk.Label(child,text = "Please enter end date in YYYY-MM-DD format: ", font = self.text_font)
        self.end_date = tk.Entry(child,font = self.text_font)
        enddate_q.pack()
        self.end_date.pack(pady=10, padx=10)

        enter = tk.Button(child,text="Get Data", width = 10, font = self.button_font, command = lambda: self.req_to_frame(self.key.get(), self.stock.get(), self.start_date.get(), self.end_date.get())) 
        enter.pack(pady=10, padx=10)
        
    def symb_names(self, keywords, key):
        #Looking up a company's symbol
        comp_stock = self.req_list_symb(self.keywords.get(), self.key.get())
        self.comp_list(comp_stock) 
    
    def req_list_symb(self, keywords, key):
        #Function that asks the user to input their key and a name
        #Returns a dictionary with a list of the companies 
        #with the most similar name
        symbol_func = "SYMBOL_SEARCH"
        symbol_url = 'https://www.alphavantage.co/query?function={}&keywords={}&apikey={}'.format(
            symbol_func, keywords, key)
        req_symb = requests.get(symbol_url)
        comp_stock = req_symb.json()
        return comp_stock
    
    def comp_list(self, comp_stock):
    #Prints out the search results for the company symbols request
        strcompanies = ""
        if len(comp_stock['bestMatches']) > 0:
            self.msg_window("Please select required symbol from options\
                        \n and click 'Enter Company Symbol' to retrieve data.")
            for index, company in enumerate(comp_stock['bestMatches']):
                strcompanies += ("Company Symbol : " + company['1. symbol'] + "\n" + 
              "Company Name : " + company['2. name'] + "\n" +
              "Stock Type : " + company['3. type'] + "\n" + 
              "Region : " + company['4. region'] + "\n" +"\n")
            self.msg_window(strcompanies)
        else:
            self.msg_window("No companies were found. Try again")
    
    def req_to_frame(self, stock, key, start_date, end_date):
        #Putting all together
        self.stock_dict = self.stock_query(self.key.get(), self.stock.get(), self.start_date.get(), self.end_date.get())
        self.get_stock_dict()
        return self.stock_dict
    
    def stock_query(self, key, stock, start_date, end_date):
        #Asks the user for a key, date range, and stock 
        #and returns a dictionary with all the requested stocks
        self.stock_dict = {}
        
        self.validate(self.start_date.get(), self.end_date.get())
        self.date_order(self.start_date.get(), self.end_date.get())
        
        funct = "TIME_SERIES_DAILY_ADJUSTED"
        self.stock_dict[self.stock.get()] = 0  
        url = 'https://www.alphavantage.co/query?function={}&symbol={}&outputsize=full&apikey={}'.format(\
                                                  funct, stock, key)
        req_stk = requests.get(url)
        stk_frame = req_stk.json()
        self.stock_dict = self.date_slicer(stk_frame, self.stock_dict, self.stock.get(), self.start_date.get(), self.end_date.get())
        return self.stock_dict
    
    def date_slicer(self, stk_frame, stock_dict, stock, start_date, end_date):
        #Returns:
        #1. The Stock dictionary updated with the dataframe
        #It also produces a csv file per stock with the data
        try:
            date_frame = pd.DataFrame(stk_frame["Time Series (Daily)"], dtype = "float").T.sort_index()
        except KeyError:
            raise tk.messagebox.showinfo("Error", "Stocks not found. Please enter a correct symbol.")
        sliced_frame = date_frame.loc[self.start_date.get():self.end_date.get()]
        self.stock_dict[self.stock.get()] = sliced_frame
        sliced_frame.to_csv("{} Data From {} to {}".format(self.stock.get(), self.start_date.get(), self.end_date.get()))
        self.msg_window("\n Data on {} from {} to {} has been retrieved.\
                        \n Please enter new information or exit the programme."
                        .format(stock, start_date, end_date))
        self.clear_text(self.stock.get(), self.start_date.get(), self.end_date.get())
        return self.stock_dict
    
    def validate(self, start_date, end_date):   
        #From jamylak
        #Validates the date format
        try:
            datetime.datetime.strptime(self.start_date.get(), '%Y-%m-%d')
        except ValueError:
            raise tk.messagebox.showinfo("Error", "Incorrect date format. Please use YYYY-MM-DD.")
        try:
            datetime.datetime.strptime(self.end_date.get(), '%Y-%m-%d')
        except ValueError:
            raise tk.messagebox.showinfo("Error", "Incorrect date format. Please use YYYY-MM-DD.")
    
    def date_order(self, start_date, end_date):
        #Checks if the date range is valid
        if self.end_date.get() <= self.start_date.get():
           raise Exception(tk.messagebox.showinfo("Error", "Invalid date range. Please try again."))
        
    def msg_window(self, msg):
        #Create message window
        child = tk.Toplevel(self.master)
        label = tk.Label(child, text = msg, font = self.text_font)
        label.pack(pady = 10, padx=10)
    
    def new_window(self):
        #Create window
        child = tk.Toplevel(self.master)
        label = tk.Label(child, font = self.text_font)
        label.pack(pady = 10, padx=10)
    
    def clear_text(self, stock, start_date, end_date):
        # Clears text after data has been retrieved
        # https://www.tutorialspoint.com/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter
        self.stock.delete(0, tk.END)
        self.start_date.delete(0, tk.END)
        self.end_date.delete(0, tk.END)
    
    def get_stock_dict(self):
        global s_dict
        s_dict = self.stock_dict
        return s_dict
        
    def quit(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    ChooseStock(root)
    root.mainloop()


