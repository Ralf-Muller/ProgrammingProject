# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 16:15:36 2021

@author: Rachel
"""
#key: 7QJ0OD6RU5IEVRO4

import requests
import pandas as pd
import datetime
import tkinter as tk

class ChooseStock():
    def __init__(self, master):
        self.master = master

        master.title("Stock Analyser")

        self.greet = tk.Label(master, text="Welcome to the Stocks Analyser.")
        self.greet.pack(pady=10)
            
        key_q = tk.Label(text="Please enter Alphavantage key: ")
        self.key = tk.Entry()
        key_q.pack()
        self.key.pack()
             
        stock_q = tk.Label(text="Please enter company symbol: ")
        self.stock = tk.Entry()
        stock_q.pack()
        self.stock.pack()
        
        start_date_q = tk.Label(text = "Please enter start date in YYYY-MM-DD format: ")
        self.start_date = tk.Entry()
        start_date_q.pack()
        self.start_date.pack()
        
        enddate_q = tk.Label(text = "Please enter end date in YYYY-MM-DD format: ")
        self.end_date = tk.Entry()
        enddate_q.pack()
        self.end_date.pack(pady=10)

        find = tk.Button(master, text="Get Data", command = lambda: self.enter_symbol(self.key.get(), self.stock.get(), self.start_date.get(), self.end_date.get()))
        find.pack(pady=10)
        
    def enter_symbol(self, key, stock, start_date, end_date):
        s_dict = self.req_to_frame(self.key.get(), self.stock.get(), self.start_date.get(), self.end_date.get())
    
    def req_to_frame(self, key, stock, start_date, end_date):
        #Putting all together
        stock_dict = self.stock_query(self.key.get(), self.stock.get(), self.start_date.get(), self.end_date.get())
        return stock_dict  
    
    def stock_query(self, key, stock, start_date, end_date):
        #Asks the user for a key, date range, and stock 
        #and returns a dictionary with all the requested stocks
        stock_dict = {}
        
        self.validate(self.start_date.get(), self.end_date.get())
        self.date_order(self.start_date.get(), self.end_date.get())
        
        funct = "TIME_SERIES_DAILY_ADJUSTED"
        stock_dict[self.stock.get()] = 0  
        url = 'https://www.alphavantage.co/query?function={}&symbol={}&outputsize=full&apikey={}'.format(\
                                                  funct, stock, key)
        req_stk = requests.get(url)
        stk_frame = req_stk.json()
        stock_dict = self.date_slicer(stk_frame, stock_dict, self.stock.get(), self.start_date.get(), self.end_date.get())
        #add in quit here
        return stock_dict
    
    def date_slicer(self, stk_frame, stock_dict, stock, start_date, end_date):
        #Returns:
        #1. The Stock dictionary updated with the dataframe
        #It also produces a csv file per stock with the data
        try:
            date_frame = pd.DataFrame(stk_frame["Time Series (Daily)"], dtype = "float").T.sort_index()
        except KeyError:
            raise tk.messagebox.showinfo("Error", "Stocks not found. Please enter a correct symbol.")
        sliced_frame = date_frame.loc[self.start_date.get():self.end_date.get()]
        stock_dict[self.stock.get()] = sliced_frame
        sliced_frame.to_csv("{} Data From {} to {}".format(self.stock.get(), self.start_date.get(), self.end_date.get()))
        self.msg_window("\n Data on {} from {} to {} has been retrieved.\
                        \n Please enter new information or exit the programme."
                        .format(stock, start_date, end_date))
        self.clear_text(self.stock.get(), self.start_date.get(), self.end_date.get())
        return stock_dict
    
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
        label = tk.Label(child, text = msg)
        label.pack()
    
    def clear_text(self, stock, start_date, end_date):
        # Clears text after data has been retrieved
        # https://www.tutorialspoint.com/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter
        self.stock.delete(0, tk.END)
        self.start_date.delete(0, tk.END)
        self.end_date.delete(0, tk.END)
    
    def quit(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    ChooseStock(root)
    root.mainloop()

            
        
        
        
        
        
        
        
        
        
        
        
        
        