

#key: 7QJ0OD6RU5IEVRO4

import tkinter as tk
import requests
import numpy as np
import pandas as pd
import datetime
import stk_requestF as stkr
import stock_info as stki
import predictive_analytics_ols as stkols
import stock_lookup as stkl


s_dict = {}

class ChooseStock:
    def __init__(self, master):
        self.master = master

        master.title("Stock Analyser")
        
        self.heading_font = ("Lato", 12, "bold")
        self.button_font = ("Lato", 11)
        self.text_font = ("Lato", 11)
        
        self.greet = tk.Label(master, text="Welcome to the Stocks Analyser.", font = self.heading_font )
        self.greet.pack(pady=10, padx=10)

        self.find = tk.Button(master, width = 20, text="Find Company Symbol", font = self.button_font, command = self.find_symbol)
        self.find.pack(pady=10, padx=10)
        self.enter = tk.Button(master, width = 20, text="Enter Company Symbol", font = self.button_font, command = self.enter_symbol)
        self.enter.pack(pady=10, padx=10)
        
        self.descr = tk.Button(master, width = 20, text="Describe me a company", font = self.button_font, command = self.describe_symbol)
        self.descr.pack(pady = 10, padx = 10)
        
        #Main buttons section
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #Main Buttons section
        exit = tk.Button(master, text="Quit", width = 20, font = self.button_font, command = self.quit)
        exit.pack(pady = 10, padx=10)
        
     #RALF
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     #RALF
        
    def describe_symbol(self):

        child = tk.Toplevel(self.master)
        stock_d = tk.Label(child,text="Please give me a downloaded stock: ", font = self.text_font)
        self.stock_d = tk.Entry(child,font = self.text_font)
        stock_d.pack(pady=5, padx=5)
        self.stock_d.pack(pady=5, padx=5)
        
        describe = tk.Button(child,text="Describe stock", width = 10, font = self.button_font, command = lambda: self.get_descr(self.dict, self.stock_d.get()))
        describe.pack(pady=10, padx=10)
        
    def get_descr(self, stk_dict, stock_d):
        self.d_values, self.str_values = stki.get_description(stk_dict, stock_d)
        self.msg_window("Adjusted closing price of {} from {} to {}: {}".format(
                stock_d, self.d_values.index[0], self.d_values.index[-1], self.str_values))
             
    def find_symbol(self):
        # Inputs to find symbol
        child = tk.Toplevel(self.master)
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
        
    def symb_names(self, keywords, key):
        self.comp_stock = stkl.req_list_symb(keywords, key)
        strcompanies = ""
        if len(self.comp_stock['bestMatches']) > 0:
            self.msg_window("Please select required symbol from options\
                        \n and click 'Enter Company Symbol' to retrieve data.")
            for index, company in enumerate(self.comp_stock['bestMatches']):
                strcompanies += ("Company Symbol : " + company['1. symbol'] + "\n" + 
              "Company Name : " + company['2. name'] + "\n" +
              "Stock Type : " + company['3. type'] + "\n" + 
              "Region : " + company['4. region'] + "\n" +"\n")
            self.msg_window(strcompanies)
        else:
            self.msg_window("No companies were found. Try again")
        
        
    def enter_symbol(self):
        # Inputs to enter symbol
        child = tk.Toplevel(self.master)

        key_q = tk.Label(child,text = "Please enter Alphavantage key : ", font = self.text_font)
        self.key = tk.Entry(child,font = self.text_font)
        key_q.pack(pady=5, padx=5)
        self.key.pack(pady=5, padx=5)
        
        stock_q = tk.Label(child,text="Please enter two company symbols (separated with comma): ", font = self.text_font)
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
        
    def req_to_frame(self, key, stock, start_date, end_date):
        #stkr.date_order(start_date, end_date)
        self.dict = stkr.req_to_frame(key, stock, start_date, end_date)
        self.msg_window("Operation Successful. Downloaded {} ".format(list(self.dict.keys())))
        
        #VINCENT
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #VINCENT
        
        #JESUS
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #JESUS
        
        
        
        
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

        
    def quit(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    ChooseStock(root)
    root.mainloop()




















