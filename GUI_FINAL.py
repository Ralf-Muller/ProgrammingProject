#Grid and stringvar solution from Code With Harry: https://www.codewithharry.com/videos/python-gui-tkinter-hindi-10
#Graph into TKINTER FROM geekforgeeks https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
#and Somraj Chodhury from stack overflow: https://stackoverflow.com/questions/59550783/embedding-a-matplotlib-graph-in-tkinter-grid-method-and-customizing-matplotl



import tkinter as tk
import requests
import numpy as np
import pandas as pd
import datetime
import stk_requestF as stkr
import stock_info as stki
import predictive_analytics_ols as stkols
import stock_lookup as stkl
from tkinter import ttk
import time_series as stkts
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#key: 7QJ0OD6RU5IEVRO4


class ChooseStock:
    def __init__(self, master):
        self.master = master

        master.title("Stock Analyser")
        master.geometry('660x400')

        self.heading_font = ("Lato", 12, "bold")
        self.button_font = ("Lato", 11)
        self.text_font = ("Lato", 11)
                
        self.greet = tk.Label(master, text="Welcome to the Stocks Analyser.", font = self.heading_font)
        self.greet.grid(row=1,column=2)

        self.find = tk.Button(master, width = 20, text="Find Company Symbol", font = self.button_font, command = self.find_symbol).grid(row=2,column=2)

        self.enter = tk.Button(master, width = 20, text="Enter Company Symbol", font = self.button_font, command = self.enter_symbol).grid(row=3,column=2)
        
        self.h_sep = ttk.Separator(master, orient='horizontal').grid(row=6, column = 0, columnspan = 5,sticky= 'we', pady=10,padx=10)

        self.heading_1 = tk.Label(master, text="Descriptive Analytics", font = self.heading_font).grid(row=8,column=1, pady=10, padx=10)
        
        self.descr = tk.Button(master, width = 20, text="Company Description", font = self.button_font).grid(row=9,column=1,pady=10,padx=10)

        self.v_sep = ttk.Separator(master,orient='vertical').grid(row=7,column=2,rowspan=5,sticky='ns')

        self.heading_2 = tk.Label(master, text="Predictive Analytics", font = self.heading_font).grid(row=8,column=3)
        self.ols = tk.Button(master, width = 20, text="OLS", font=self.button_font).grid(row=9,column=3)

        self.stats = tk.Button(master, width = 20, text = "Basic Statistics", font = self.button_font, command = self.describe_symbol).grid(row= 10,column=1,pady=10,padx=10)

        self.visualization = tk.Button(master, width = 20, text = "Visualization", font = self.button_font).grid(row=11,column=1,pady=10,padx=10)
        
        self.time_series = tk.Button(master, width = 20, text = "Time Series", font = self.button_font, command = self.time_series_menu).grid(row=10,column=3,pady=10,padx=10)
         
        tk.Button(master, text="Quit", width = 20, font = self.button_font, command = self.quit).grid(row=12,column=2,pady=10,padx=10)


        #Main buttons section
    """Functions for calling symbols"""

    def find_symbol(self):
        # Inputs to find symbol
        child = tk.Toplevel(self.master)
        
        self.key_find = tk.StringVar()
        self.keywords_find = tk.StringVar()
        
        tk.Label(child,text="Please enter Alphavantage key: ", font = self.text_font).grid(row = 1, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.key_find).grid(row = 2, column = 1, pady=5, padx=5)
             
        tk.Label(child,text="Please enter company name: ", font = self.text_font).grid(row = 3, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.keywords_find).grid(row = 4, column = 1, pady=5, padx=5)
              
        tk.Button(child,text="Search", width = 10, font = self.button_font, command = lambda : self.symb_names(self.keywords_find.get(), self.key_find.get())).grid(row = 6, column = 1, pady=10, padx=10)

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
                
    """Functions for requesting symbols"""
    
    def enter_symbol(self):
        # Inputs to enter symbol
        child = tk.Toplevel(self.master)
        
        self.key_enter = tk.StringVar()
        self.stocks_enter = tk.StringVar()
        self.start_date_enter = tk.StringVar()
        self.end_date_enter = tk.StringVar()

        tk.Label(child,text = "Please enter Alphavantage key : ", font = self.text_font).grid(row = 1, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.key_enter).grid(row = 2, column = 1, pady=5, padx=5)

        tk.Label(child,text="Please enter two company symbols (separated with comma): ", font = self.text_font).grid(row = 3, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stocks_enter).grid(row = 4, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please enter start date in YYYY-MM-DD format: ", font = self.text_font).grid(row = 5, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.start_date_enter).grid(row = 6, column = 1, pady=5, padx=5)
   
        tk.Label(child,text = "Please enter end date in YYYY-MM-DD format: ", font = self.text_font).grid(row = 7, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.end_date_enter).grid(row = 8, column = 1, pady=5, padx=5)

        tk.Button(child,text="Get Data", width = 10, font = self.button_font, command = lambda: self.req_to_frame(self.key_enter.get(), self.stocks_enter.get(), self.start_date_enter.get(), self.end_date_enter.get())).grid(row = 9, column = 1, pady=5, padx=5) 

        
    def req_to_frame(self, key, stock, start_date, end_date):
        #stkr.date_order(start_date, end_date)
        self.dict = stkr.req_to_frame(key, stock, start_date, end_date)
        self.msg_window("Operation Successful. Downloaded {} ".format(list(self.dict.keys()))) 
        
    """Functions for getting a stock basic statistics"""
    
    
    def describe_symbol(self):

        child = tk.Toplevel(self.master)
        
        self.stock_d = tk.StringVar()

        tk.Label(child,text="Please give me a downloaded stock: ", font = self.text_font).grid(row = 1, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stock_d).grid(row = 2, column = 1, pady=5, padx=5)

        tk.Button(child,text="Describe stock", width = 10, font = self.button_font, command = lambda: self.get_descr(self.dict, self.stock_d.get())).grid(row = 3, column = 1, pady=5, padx=5)
        
    def get_descr(self, stk_dict, stock_d):
        self.d_values, self.str_values = stki.get_description(stk_dict, stock_d)
        self.msg_window("Adjusted closing price of {} from {} to {}: {}".format(
                stock_d, self.d_values.index[0], self.d_values.index[-1], self.str_values))
        
#SPACE FOR REST OF THE BUTTONS AND FUNCTIONS        
#OVERVIEW









#VISUALIZATIONS









































#TIME SERIES
    """Function for Time Series Menu"""
    
    def time_series_menu(self):
        child = tk.Toplevel(self.master)

        tk.Label(child, text="Welcome to the Time Series Menu", font = self.heading_font).grid(row= 0,column= 2)

        tk.Button(child, width = 20, text= "Correlogram", font = self.button_font, command = self.correlograms).grid(row=1,column=1)
        tk.Button(child, width = 20, text= "ARIMA", font = self.button_font).grid(row=1,column=3)
        tk.Button(child, width = 20, text= "Cointegration", font = self.button_font, command = self.cointegration).grid(row=3,column=1)
        tk.Button(child, width = 20, text= "Exponential smoothing", font = self.button_font).grid(row=3,column=3)


    def cointegration(self):

        child = tk.Toplevel(self.master)

        self.stock1_coint = tk.StringVar()
        self.stock2_coint = tk.StringVar()
        self.decis_coint = tk.StringVar()

        tk.Label(child,text = "Please give me the first stock : ", font = self.text_font).grid(row = 1, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stock1_coint).grid(row = 2, column = 1, pady=5, padx=5)


        tk.Label(child,text = "Please give me the second stock : ", font = self.text_font).grid(row = 3, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stock2_coint).grid(row = 4, column = 1, pady=5, padx=5)


        tk.Label(child,text = "Input 1 for Adjusted Close and anything else for Close " , font = self.text_font).grid(row = 5, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.decis_coint).grid(row = 6, column = 1, pady=5, padx=5)

        tk.Button(child,text="Produce test", width = 10, font = self.button_font, command = lambda : self.coint_test(self.dict, self.stock1_coint.get(), self.stock2_coint.get(), self.decis_coint.get())).grid(row = 7, column = 1, pady=10, padx=10)


    def coint_test(self, stk_dict, stock1, stock2, decis):
        self.coint_string = stkts.co_integration(stk_dict, stock1, stock2, decis)
        self.msg_window(self.coint_string)



    #def test_graph(self):
        
       # child = tk.Toplevel(self.master)

        #self.x = ["Col A", "Col B"]
        #self.y = [50, 20]
        
       # fig = plt.figure(figsize = (4, 5))
       # plt.bar(x = self.x, height = self.y)
        
       # canvas = FigureCanvasTkAgg(fig, master = child)
       # canvas.draw()
       # canvas.get_tk_widget().grid(row = 1, column = 0, ipadx = 40, ipady = 20)
        
        #toolbarFrame = tk.Frame(master = child)
        #toolbarFrame.grid(row = 2, column = 0)
        #toolbar = NavigationToolbar2Tk(canvas, toolbarFrame) 
        #toolbar.update()
        
    def correlograms(self):
        
        child = tk.Toplevel(self.master)
        
        self.stock_corr = tk.StringVar()
        self.diff_corr = tk.StringVar()
        self.decis_corr = tk.StringVar()
        self.lags_corr = tk.StringVar()

        tk.Label(child,text = "Please give me a stock : ", font = self.text_font).grid(row = 1, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stock_corr).grid(row = 2, column = 1, pady=5, padx=5)


        tk.Label(child,text = "Please give me the number of lags : ", font = self.text_font).grid(row = 3, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.lags_corr).grid(row = 4, column = 1, pady=5, padx=5)


        tk.Label(child,text = "Input 1 for Adjusted Close and anything else for Close " , font = self.text_font).grid(row = 5, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.decis_corr).grid(row = 6, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Input 1 for First Differences and anything else for normal " , font = self.text_font).grid(row = 7, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.diff_corr).grid(row = 8, column = 1, pady=5, padx=5)

        tk.Button(child,text="Produce test", width = 10, font = self.button_font, command = lambda : self.show_correlogram(self.dict, self.stock_corr.get(), self.diff_corr.get(), self.lags_corr.get(), self.decis_corr.get())).grid(row = 9, column = 1, pady=10, padx=10)

    def show_correlogram(self, s_dict, stock, diff, lags, decis):
        
        child = tk.Toplevel(self.master)
        
        self.acf, self.pacf = stkts.correlogram(self.dict, stock, diff, lags, decis)
        
        canvas_acf = FigureCanvasTkAgg(self.acf, master = child)
        canvas_acf.draw()
        canvas_acf.get_tk_widget().grid(row = 1, column = 0, ipadx = 40, ipady = 20)
        
        canvas_pacf = FigureCanvasTkAgg(self.pacf, master = child)
        canvas_pacf.draw()
        canvas_pacf.get_tk_widget().grid(row = 2, column = 0, ipadx = 40, ipady = 20)























        
     
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



















