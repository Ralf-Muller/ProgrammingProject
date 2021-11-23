#Grid and stringvar solution from Code With Harry: https://www.codewithharry.com/videos/python-gui-tkinter-hindi-10
#Graph into TKINTER FROM geekforgeeks https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
#and Somraj Chodhury from stack overflow: https://stackoverflow.com/questions/59550783/embedding-a-matplotlib-graph-in-tkinter-grid-method-and-customizing-matplotl


import copy
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
import date_as_floating_value as datef
import visualizations as vs
#key: 7QJ0OD6RU5IEVRO4


class ChooseStock:
    def __init__(self, master):
        self.master = master
        
        self.dict = {}

        master.title("Stock Analyser")
        master.geometry('1600x900')

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
        self.ols = tk.Button(master, width = 20, text="OLS", font=self.button_font, command = self.ols_menu).grid(row=9,column=3)

        self.stats = tk.Button(master, width = 20, text = "Basic Statistics", font = self.button_font, command = self.describe_symbol).grid(row= 10,column=1,pady=10,padx=10)

        self.visualization = tk.Button(master, width = 20, text = "Visualization", font = self.button_font, command=self.visualisations_menu).grid(row=11,column=1,pady=10,padx=10)
        
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

        tk.Label(child,text="Please enter a stock to download: ", font = self.text_font).grid(row = 3, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stocks_enter).grid(row = 4, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please enter start date in YYYY-MM-DD format: ", font = self.text_font).grid(row = 5, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.start_date_enter).grid(row = 6, column = 1, pady=5, padx=5)
   
        tk.Label(child,text = "Please enter end date in YYYY-MM-DD format: ", font = self.text_font).grid(row = 7, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.end_date_enter).grid(row = 8, column = 1, pady=5, padx=5)

        tk.Button(child,text="Get Data", width = 10, font = self.button_font, command = lambda: self.req_to_frame(self.dict, self.key_enter.get(), self.stocks_enter.get(), self.start_date_enter.get(), self.end_date_enter.get())).grid(row = 9, column = 1, pady=5, padx=5) 

        
    def req_to_frame(self, stock_dict, key, stock, start_date, end_date):
        #stkr.date_order(start_date, end_date)
        self.dict = stkr.req_to_frame(stock_dict, key, stock, start_date, end_date)
        self.dict2 = datef._mutate_date_(copy.deepcopy(self.dict))
        self.msg_window("Operation Successful. Downloaded {} ".format(list(self.dict.keys()))) 
        
    """Functions for getting a stock basic statistics"""
    
    
    def describe_symbol(self):

        child = tk.Toplevel(self.master)
        
        self.stock_d = tk.StringVar()

        tk.Label(child,text="Please give me a downloaded stock: ", font = self.text_font).grid(row = 1, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stock_d).grid(row = 2, column = 1, pady=5, padx=5)

        tk.Button(child,text="Describe stock", width = 15, font = self.button_font, command = lambda: self.get_descr(self.dict, self.stock_d.get())).grid(row = 3, column = 1, pady=5, padx=5)
        
    def get_descr(self, stk_dict, stock_d):
        self.d_values, self.str_values = stki.get_description(stk_dict, stock_d)
        self.msg_window("Adjusted closing price of {} from {} to {}: {}".format(
                stock_d, self.d_values.index[0], self.d_values.index[-1], self.str_values))
        
#SPACE FOR REST OF THE BUTTONS AND FUNCTIONS        
#OVERVIEW










## OLS
    def ols_menu(self):
        
        child = tk.Toplevel(self.master)

        tk.Label(child, text="Welcome to the Linear Regression Menu", font = self.heading_font).grid(row= 0,column= 2)

        tk.Button(child, width = 20, text= "OLS With 2 Stocks", font = self.button_font, command = self.ols_2_stocks).grid(row=1,column=1)
        tk.Button(child, width = 20, text= "OLS With 1 Stock", font = self.button_font, command = self.ols_1_stock).grid(row=1,column=3)    
    
    def ols_2_stocks(self):
        child = tk.Toplevel(self.master)
        stock_ols2 = tk.Label(child,text="For which stocks do you wish to make your analysis (separated with comma): " + ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_ols2 = tk.Entry(child,font = self.text_font)
        self.stock_ols2.grid(row=2,column=1,pady=5,padx=5)
        
        stock_olst = tk.Label(child,text="Please select the Test Size as a decimal point: ", font = self.text_font).grid(row=3,column=1,pady=5,padx=5)
        self.stock_olst = tk.Entry(child,font = self.text_font)
        self.stock_olst.grid(row=4,column=1,pady=5,padx=5) 
        
        describe = tk.Button(child,text="Analyse stocks", width = 10, font = self.button_font, command = lambda: self.get_ols2(self.dict2, self.stock_ols2.get(), self.stock_olst.get())).grid(row=5,column=1,pady=5,padx=5)

    def get_ols2(self, dict2, stocks, t_size):       
        companies = stocks.split(',')
        ols2str = stkols.OLS_two_stocks(dict2, companies, t_size)
        self.msg_window(ols2str)

    def ols_1_stock(self):
        child = tk.Toplevel(self.master)
        stock_ols = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_ols = tk.Entry(child,font = self.text_font)
        self.stock_ols.grid(row=2,column=1,pady=5,padx=5)
        
        stock_olst = tk.Label(child,text="Please select the Test Size as a decimal point: ", font = self.text_font).grid(row=3,column=1,pady=5,padx=5)
        self.stock_olst = tk.Entry(child,font = self.text_font)
        self.stock_olst.grid(row=4,column=1,pady=5,padx=5)
        
        dateols = tk.Label(child,text="For which date do you wish to know the prediction? \nPlease use YYYY-MM-DD format: ", font = self.text_font).grid(row=5,column=1,pady=5,padx=5)
        self.dateols = tk.Entry(child,font = self.text_font)
        self.dateols.grid(row=6,column=1,pady=5,padx=5)
        
        describe = tk.Button(child,text="Analyse stocks", width = 10, font = self.button_font, command = lambda: self.get_ols(self.dict2, self.stock_ols.get(), self.stock_olst.get(), self.dateols.get())).grid(row=7,column=1,pady=5,padx=5)

    def get_ols(self, dict2, stocks, t_size, date): 
        companies = stocks.split(',')
        ols2str = stkols.sk_predval_OLS(dict2, companies, t_size, date)
        self.msg_window(ols2str)

 ## Visualisations
 
    def visualisations_menu(self):
        child = tk.Toplevel(self.master)

        tk.Label(child, text="Please select a visualisation from list below", font = self.heading_font).grid(row= 0,column= 2)

        self.raw = tk.Button(child, width = 20, text="Raw Time Series", font = self.button_font, command = self.raw_ts).grid(row=3,column=1,pady=5,padx=5)           
        self.trend = tk.Button(child, width = 20, text="Trend Line", font = self.button_font, command = self.trend).grid(row=4,column=1,pady=5,padx=5)     
        self.sma = tk.Button(child, width = 20, text="Moving Averages", font = self.button_font, command = self.sma).grid(row=5,column=1,pady=5,padx=5)           
        self.bband = tk.Button(child, width = 20, text="Bollinger Bands", font = self.button_font, command = self.bollinger).grid(row=2,column=1,pady=5,padx=5) 
        self.wsma = tk.Button(child, width = 20, text="Weighted Moving Averages", font = self.button_font, command = self.wma).grid(row=2,column=3,pady=5,padx=5)    
        self.bmacd = tk.Button(child, width = 20, text="MACD", font = self.button_font, command = self.macd).grid(row=3,column=3,pady=5,padx=5)    
        self.brsi = tk.Button(child, width = 20, text="RSI", font = self.button_font, command = self.rsi).grid(row=4,column=3,pady=5,padx=5)        
        self.autocorrel = tk.Button(child, width = 20, text="Autocorrelation", font = self.button_font, command = self.auto_c).grid(row=5,column=3,pady=5,padx=5)


    def raw_ts(self):
        child = tk.Toplevel(self.master)

        stock_raw = tk.Label(child,text="For which company do you wish to make your analysis: "+ ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_raw = tk.Entry(child,font = self.text_font)
        self.stock_raw.grid(row=2,column=1,pady=5,padx=5)
        
        describe = tk.Button(child,text="Plot Stock", width = 10, font = self.button_font, command = lambda: self.get_raw(self.dict2, self.stock_raw.get())).grid(row=3,column=1,pady=5,padx=5)

    def get_raw(self, dict2, company):       
        companies = company.split(',')
        vs.raw_time_series(dict2, companies)    
    
    
    def trend(self):
        child = tk.Toplevel(self.master)
        s_trend = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.s_trend = tk.Entry(child,font = self.text_font)
        self.s_trend.grid(row=2,column=1,pady=5,padx=5)
        
        stock_olst = tk.Label(child,text="Please select the Test Size as a decimal point: ", font = self.text_font).grid(row=3,column=1,pady=5,padx=5)
        self.stock_olst = tk.Entry(child,font = self.text_font)
        self.stock_olst.grid(row=4,column=1,pady=5,padx=5)
        
        describe = tk.Button(child,text="Plot Stock", width = 10, font = self.button_font, command = lambda: self.get_trend(self.dict2, self.s_trend.get(), self.stock_olst.get())).grid(row=5,column=1,pady=5,padx=5)

    def get_trend(self, dict2, stocks, t_size): 
        companies = stocks.split(',')
        vs.plot_trend_line(dict2, companies, t_size)

    def sma(self):
        child = tk.Toplevel(self.master)
        stock_sma = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_sma = tk.Entry(child,font = self.text_font)
        self.stock_sma.grid(row=2,column=1,pady=5,padx=5)
        
        sma_win = tk.Label(child,text="Please select the Window Size: ", font = self.text_font).grid(row=3,column=1,pady=5,padx=5)
        self.sma_win = tk.Entry(child,font = self.text_font)
        self.sma_win.grid(row=4,column=1,pady=5,padx=5)

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_sma(self.dict2, self.stock_sma.get(), self.sma_win.get())).grid(row=5,column=1,pady=5,padx=5)

    def get_sma(self, dict2, stocks, win_size): 
        companies = stocks.split(',')
        vs.plot_sma(dict2, companies, win_size)

    def wma(self):
        child = tk.Toplevel(self.master)
        stock_wma = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_wma = tk.Entry(child,font = self.text_font)
        self.stock_wma.grid(row=2,column=1,pady=5,padx=5)
        
        wma_win = tk.Label(child,text="Please select the Window Size: ", font = self.text_font).grid(row=3,column=1,pady=5,padx=5)
        self.wma_win = tk.Entry(child,font = self.text_font)
        self.wma_win.grid(row=4,column=1,pady=5,padx=5)

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_wma(self.dict2, self.stock_wma.get(), self.wma_win.get())).grid(row=5,column=1,pady=5,padx=5)

    def get_wma(self, dict2, stocks, win_size): 
        companies = stocks.split(',')
        vs.plot_wma(dict2, companies, win_size)

    def bollinger(self):
        child = tk.Toplevel(self.master)
        stock_sma = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_sma = tk.Entry(child,font = self.text_font)
        self.stock_sma.grid(row=2,column=1,pady=5,padx=5)
        
        sma_win = tk.Label(child,text="Please select the Window Size: ", font = self.text_font).grid(row=3,column=1,pady=5,padx=5)
        self.sma_win = tk.Entry(child,font = self.text_font)
        self.sma_win.grid(row=4,column=1,pady=5,padx=5)
        
        stdev = tk.Label(child,text='How many standard deviations away from the mean do you wish to calculate? ', font = self.text_font).grid(row=5,column=1,pady=5,padx=5)
        self.stdev = tk.Entry(child,font = self.text_font)
        self.stdev.grid(row=6,column=1,pady=5,padx=5)
        
        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_bollinger(self.dict2, self.stock_sma.get(), self.sma_win.get(), self.stdev.get())).grid(row=7,column=1,pady=5,padx=5)

    def get_bollinger(self, dict2, stocks, win_size, stdev): 
        companies = stocks.split(',')
        vs.plot_bollinger(dict2, companies, win_size, stdev)

    def macd(self):
        child = tk.Toplevel(self.master)
        stock_macd = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_macd = tk.Entry(child,font = self.text_font)
        self.stock_macd.grid(row=2,column=1,pady=5,padx=5)
        
        fema = tk.Label(child,text="Please enter the length of the Fast EMA: ", font = self.text_font).grid(row=3,column=1,pady=5,padx=5)
        self.fema = tk.Entry(child,font = self.text_font)
        self.fema.grid(row=4,column=1,pady=5,padx=5)
        
        sema = tk.Label(child,text="Please enter the length of the Slow EMA: ", font = self.text_font).grid(row=5,column=1,pady=5,padx=5)
        self.sema = tk.Entry(child,font = self.text_font)
        self.sema.grid(row=6,column=1,pady=5,padx=5)
        
        smooth = tk.Label(child,text="Please enter the period of the Signal Line", font = self.text_font).grid(row=7,column=1,pady=5,padx=5)
        self.smooth = tk.Entry(child,font = self.text_font)
        self.smooth.grid(row=8,column=1,pady=5,padx=5)

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_macd(self.dict2, self.stock_macd.get(), self.fema.get(), self.sema.get(), self.smooth.get())).grid(row=9,column=1,pady=5,padx=5)

    def get_macd(self, dict2, stocks, fema, sema, smooth): 
        companies = stocks.split(',')
        vs.plot_macd(dict2, companies, fema, sema, smooth)    

    def rsi(self):
        child = tk.Toplevel(self.master)
        stock_rsi = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_rsi = tk.Entry(child,font = self.text_font)
        self.stock_rsi.grid(row=2,column=1,pady=5,padx=5)
        
        sma_win = tk.Label(child,text="Please select the Window Size: ", font = self.text_font).grid(row=3,column=1,pady=5,padx=5)
        self.sma_win = tk.Entry(child,font = self.text_font)
        self.sma_win.grid(row=4,column=1,pady=5,padx=5)

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_rsi(self.dict2, self.stock_rsi.get(), self.sma_win.get())).grid(row=5,column=1,pady=5,padx=5)

    def get_rsi(self, dict2, stocks, win_size): 
        companies = stocks.split(',')
        vs.plot_rsi(dict2, companies, win_size)    

    def auto_c(self):
        child = tk.Toplevel(self.master)
        stock_raw = tk.Label(child,text="For which company do you wish to make your analysis: "+ ', '.join(list(self.dict.keys())), font = self.text_font).grid(row=1,column=1,pady=5,padx=5)
        self.stock_raw = tk.Entry(child,font = self.text_font)
        self.stock_raw.grid(row=2,column=1,pady=5,padx=5)
        
        describe = tk.Button(child,text="Plot Stock", width = 10, font = self.button_font, command = lambda: self.get_auto_c(self.dict2, self.stock_raw.get())).grid(row=3,column=1,pady=5,padx=5)

    def get_auto_c(self, dict2, company):       
        companies = company.split(',')
        vs.auto_correl(dict2, companies)


#TIME SERIES
    """Function for Time Series Menu"""
    
    def time_series_menu(self):
        child = tk.Toplevel(self.master)

        tk.Label(child, text="Welcome to the Time Series Menu", font = self.heading_font).grid(row= 0,column= 2)

        tk.Button(child, width = 20, text= "Correlogram", font = self.button_font, command = self.correlograms).grid(row=1,column=1)
        tk.Button(child, width = 20, text= "ARIMA", font = self.button_font, command = self.arima_menu).grid(row=1,column=3)
        tk.Button(child, width = 20, text= "Cointegration", font = self.button_font, command = self.cointegration).grid(row=3,column=1)
        tk.Button(child, width = 20, text= "Exponential smoothing", font = self.button_font, command = self.exponential_menu).grid(row=3,column=3)


    """Functions for cointegration test"""

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
        if stk_dict[stock1].index.equals(stk_dict[stock2].index) != True:
            raise tk.messagebox.showerror("Error",'Dates do not match')
        self.coint_string = stkts.co_integration(stk_dict, stock1, stock2, decis)
        self.msg_window(self.coint_string)

    """Functions for correlograms"""
        
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
        
        stkts.correlogram(self.dict, stock, diff, lags, decis)      

    """Functions for arima"""

    def arima_menu(self):
        
        child = tk.Toplevel(self.master)
        
        self.stock_arima = tk.StringVar()
        self.decis_arima = tk.StringVar()
        self.ord_q_arima = tk.StringVar()
        self.ord_p_arima = tk.StringVar()
        self.ord_d_arima = tk.StringVar()
        self.pred_days_arima = tk.StringVar()
        self.start_date_arima = tk.StringVar()
        
        
        tk.Label(child,text = "Please give me the stock : ", font = self.text_font).grid(row = 1, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stock_arima).grid(row = 2, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please give me the AR order p : ", font = self.text_font).grid(row = 3, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.ord_p_arima).grid(row = 4, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please give me the Differences order d : ", font = self.text_font).grid(row = 5, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.ord_d_arima).grid(row = 6, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please give me the MA order q : ", font = self.text_font).grid(row = 7, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.ord_q_arima).grid(row = 8, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please give me the number of days to predicts : ", font = self.text_font).grid(row = 9, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.pred_days_arima).grid(row = 10, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please give me the start date of the prediction : ", font = self.text_font).grid(row = 11, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.start_date_arima).grid(row = 12, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Input 1 for Adjusted Close and anything else for Close " , font = self.text_font).grid(row = 13, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.decis_arima).grid(row = 14, column = 1, pady=5, padx=5)

        tk.Button(child,text="Produce ARIMA", width = 10, font = self.button_font, command = lambda : self.arima_maker(
                self.dict, self.stock_arima.get(), self.decis_arima.get(), 
                self.ord_p_arima.get(), self.ord_d_arima.get(), self.ord_q_arima.get(),
                self.pred_days_arima.get(), self.start_date_arima.get())).grid(row = 15, column = 1, pady=10, padx=10)


    def arima_maker(self, s_dict, stock, decis, order_p, order_dif, order_q, pred_days, start_date):
        self.arima_res = stkts.make_arima(s_dict, stock, decis, order_p, order_dif, order_q, pred_days, start_date)
        self.msg_window(self.arima_res)
        
    """Functions for exponential"""
       
    def exponential_menu(self):
        
        child = tk.Toplevel(self.master)

        self.stock_exp = tk.StringVar()
        self.decis_exp = tk.StringVar()
        self.user_exp = tk.StringVar()
        self.damp_exp = tk.StringVar()
        self.smooth_exp = tk.StringVar()
        self.end_date_exp = tk.StringVar()
        self.start_date_exp = tk.StringVar()
        
        tk.Label(child,text = "Please give me the stock : ", font = self.text_font).grid(row = 1, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.stock_exp).grid(row = 2, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Feed a date to start the prediction YYYY-MM-DD \
                 PLEASE WRITE A DATE LATER THAN THE FIRST AVAILABLE DATE", font = self.text_font).grid(row = 3, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.start_date_exp).grid(row = 4, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Feed a date to end the prediction YYYY-MM-DD: \
                 PLEASE WRITE A DATE LATER THAN THE FIRST AVAILABLE DATE", font = self.text_font).grid(row = 5, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.end_date_exp).grid(row = 6, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please feed me a smoothing level for Simple Exponential Smoothing : ", font = self.text_font).grid(row = 7, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.smooth_exp).grid(row = 8, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please feed me a damping slope for Holt's Additive Model : ", font = self.text_font).grid(row = 9, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.damp_exp).grid(row = 10, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Please write the options you want: \n \
                 Ex. '01234' \n \
                 0. Simple Exponential Smoothing \n \
                 1. Holt Standard \n \
                 2. Holt Exponential \n \
                 3. Holt Additive Damped \n \
                 4. Holt Multiplicative Damped ", font = self.text_font).grid(row = 11, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.user_exp).grid(row = 12, column = 1, pady=5, padx=5)

        tk.Label(child,text = "Input 1 for Adjusted Close and anything else for Close " , font = self.text_font).grid(row = 13, column = 1, pady=5, padx=5)
        tk.Entry(child,font = self.text_font, textvariable = self.decis_exp).grid(row = 14, column = 1, pady=5, padx=5)
        
        tk.Button(child,text="Produce Graphs", width = 10, font = self.button_font, command = lambda : self.exp_maker(
                self.dict, self.stock_exp.get(), self.decis_exp.get(), 
                self.start_date_exp.get(), self.end_date_exp.get(), self.smooth_exp.get(),
                self.damp_exp.get(), self.user_exp.get())).grid(row = 15, column = 1, pady=10, padx=10)
    
    def exp_maker(self, s_dict, stock, decis, start_date, end_date, smooth, damp, user_choice):
        stkts.exponential_graphs(s_dict, stock, decis, start_date, end_date, smooth, damp, user_choice)
     
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




















