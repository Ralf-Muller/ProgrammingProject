

#key: 7QJ0OD6RU5IEVRO4
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
import date_as_floating_value as datef
import visualizations as vs

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
        self.ols2 = tk.Button(master, width = 20, text="OLS Two Stocks", font = self.button_font, command = self.ols_2_stocks)
        self.ols2.pack(pady = 10, padx = 10)        
        
        self.ols2 = tk.Button(master, width = 20, text="OLS Prediction", font = self.button_font, command = self.ols_1_stock)
        self.ols2.pack(pady = 10, padx = 10)               
        
        self.raw = tk.Button(master, width = 20, text="Raw Time Series", font = self.button_font, command = self.raw_ts)
        self.raw.pack(pady = 10, padx = 10)               
                
        self.trend = tk.Button(master, width = 20, text="Trend Line", font = self.button_font, command = self.trend)
        self.trend.pack(pady = 10, padx = 10)         
        
        self.sma = tk.Button(master, width = 20, text="Moving Averages", font = self.button_font, command = self.sma)
        self.sma.pack(pady = 10, padx = 10)             
        
        self.bband = tk.Button(master, width = 20, text="Bollinger Bands", font = self.button_font, command = self.bollinger)
        self.bband.pack(pady = 10, padx = 10)         
        
        self.wsma = tk.Button(master, width = 20, text="Weighted Moving Averages", font = self.button_font, command = self.wma)
        self.wsma.pack(pady = 10, padx = 10)        
        
        self.bmacd = tk.Button(master, width = 20, text="MACD", font = self.button_font, command = self.macd)
        self.bmacd.pack(pady = 10, padx = 10)        
        
        self.brsi = tk.Button(master, width = 20, text="RSI", font = self.button_font, command = self.rsi)
        self.brsi.pack(pady = 10, padx = 10)          
        
        self.autocorrel = tk.Button(master, width = 20, text="Autocorrelation", font = self.button_font, command = self.auto_c)
        self.autocorrel.pack(pady = 10, padx = 10)         
        
        
        
        
        #Main Buttons section
        exit = tk.Button(master, text="Quit", width = 20, font = self.button_font, command = self.quit)
        exit.pack(pady = 10, padx=10)
        
     #RALF
    def ols_2_stocks(self):
        child = tk.Toplevel(self.master)
        stock_ols2 = tk.Label(child,text="For which stocks do you wish to make your analysis (separated with comma): " + ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_ols2 = tk.Entry(child,font = self.text_font)
        stock_ols2.pack(pady=5, padx=5)
        self.stock_ols2.pack(pady=5, padx=5)
        
        stock_olst = tk.Label(child,text="Please select the Test Size as a decimal point: ", font = self.text_font)
        self.stock_olst = tk.Entry(child,font = self.text_font)
        stock_olst.pack(pady=5, padx=5)
        self.stock_olst.pack(pady=5, padx=5)        
        
        describe = tk.Button(child,text="Analyse stocks", width = 10, font = self.button_font, command = lambda: self.get_ols2(self.dict2, self.stock_ols2.get(), self.stock_olst.get()))
        describe.pack(pady=10, padx=10)   
     
    def get_ols2(self, dict2, stocks, t_size):       
        companies = stocks.split(',')
        ols2str = stkols.OLS_two_stocks(dict2, companies, t_size)
        self.msg_window(ols2str)
        
    def ols_1_stock(self):
        child = tk.Toplevel(self.master)
        stock_ols = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_ols = tk.Entry(child,font = self.text_font)
        stock_ols.pack(pady=5, padx=5)
        self.stock_ols.pack(pady=5, padx=5)
        
        stock_olst = tk.Label(child,text="Please select the Test Size as a decimal point: ", font = self.text_font)
        self.stock_olst = tk.Entry(child,font = self.text_font)
        stock_olst.pack(pady=5, padx=5)
        self.stock_olst.pack(pady=5, padx=5)  
        
        dateols = tk.Label(child,text="For which date do you wish to know the prediction? \nPlease use YYYY-MM-DD format: ", font = self.text_font)
        self.dateols = tk.Entry(child,font = self.text_font)
        dateols.pack(pady=5, padx=5)
        self.dateols.pack(pady=5, padx=5)    
        
        describe = tk.Button(child,text="Analyse stocks", width = 10, font = self.button_font, command = lambda: self.get_ols(self.dict2, self.stock_ols.get(), self.stock_olst.get(), self.dateols.get()))
        describe.pack(pady=10, padx=10)                 

    def get_ols(self, dict2, stocks, t_size, date): 
        companies = stocks.split(',')
        ols2str = stkols.sk_predval_OLS(dict2, companies, t_size, date)
        self.msg_window(ols2str)

    
    def raw_ts(self):
        child = tk.Toplevel(self.master)
        stock_raw = tk.Label(child,text="For which company do you wish to make your analysis: "+ ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_raw = tk.Entry(child,font = self.text_font)
        stock_raw.pack(pady=5, padx=5)
        self.stock_raw.pack(pady=5, padx=5)       
        
        describe = tk.Button(child,text="Plot Stock", width = 10, font = self.button_font, command = lambda: self.get_raw(self.dict2, self.stock_raw.get()))
        describe.pack(pady=10, padx=10)   
     
    def get_raw(self, dict2, company):       
        companies = company.split(',')
        vs.raw_time_series(dict2, companies)

    def trend(self):
        child = tk.Toplevel(self.master)
        s_trend = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font)
        self.s_trend = tk.Entry(child,font = self.text_font)
        s_trend.pack(pady=5, padx=5)
        self.s_trend.pack(pady=5, padx=5)
        
        stock_olst = tk.Label(child,text="Please select the Test Size as a decimal point: ", font = self.text_font)
        self.stock_olst = tk.Entry(child,font = self.text_font)
        stock_olst.pack(pady=5, padx=5)
        self.stock_olst.pack(pady=5, padx=5)  
        
        describe = tk.Button(child,text="Plot Stock", width = 10, font = self.button_font, command = lambda: self.get_trend(self.dict2, self.s_trend.get(), self.stock_olst.get()))
        describe.pack(pady=10, padx=10)                 

    def get_trend(self, dict2, stocks, t_size): 
        companies = stocks.split(',')
        vs.plot_trend_line(dict2, companies, t_size)

     
    def sma(self):
        child = tk.Toplevel(self.master)
        stock_sma = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_sma = tk.Entry(child,font = self.text_font)
        stock_sma.pack(pady=5, padx=5)
        self.stock_sma.pack(pady=5, padx=5)
        
        sma_win = tk.Label(child,text="Please select the Window Size: ", font = self.text_font)
        self.sma_win = tk.Entry(child,font = self.text_font)
        sma_win.pack(pady=5, padx=5)
        self.sma_win.pack(pady=5, padx=5)  

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_sma(self.dict2, self.stock_sma.get(), self.sma_win.get()))
        describe.pack(pady=10, padx=10)                 

    def get_sma(self, dict2, stocks, win_size): 
        companies = stocks.split(',')
        vs.plot_sma(dict2, companies, win_size)
 
        
    def wma(self):
        child = tk.Toplevel(self.master)
        stock_wma = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_wma = tk.Entry(child,font = self.text_font)
        stock_wma.pack(pady=5, padx=5)
        self.stock_wma.pack(pady=5, padx=5)
        
        wma_win = tk.Label(child,text="Please select the Window Size: ", font = self.text_font)
        self.wma_win = tk.Entry(child,font = self.text_font)
        wma_win.pack(pady=5, padx=5)
        self.wma_win.pack(pady=5, padx=5)  

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_wma(self.dict2, self.stock_wma.get(), self.wma_win.get()))
        describe.pack(pady=10, padx=10)                 

    def get_wma(self, dict2, stocks, win_size): 
        companies = stocks.split(',')
        vs.plot_wma(dict2, companies, win_size)

     
    def bollinger(self):
        child = tk.Toplevel(self.master)
        stock_sma = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_sma = tk.Entry(child,font = self.text_font)
        stock_sma.pack(pady=5, padx=5)
        self.stock_sma.pack(pady=5, padx=5)
        
        sma_win = tk.Label(child,text="Please select the Window Size: ", font = self.text_font)
        self.sma_win = tk.Entry(child,font = self.text_font)
        sma_win.pack(pady=5, padx=5)
        self.sma_win.pack(pady=5, padx=5)
        
        stdev = tk.Label(child,text='How many standard deviations away from the mean do you wish to calculate? ', font = self.text_font)
        self.stdev = tk.Entry(child,font = self.text_font)
        stdev.pack(pady=5, padx=5)
        self.stdev.pack(pady=5, padx=5) 

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_bollinger(self.dict2, self.stock_sma.get(), self.sma_win.get(), self.stdev.get()))
        describe.pack(pady=10, padx=10)                 

    def get_bollinger(self, dict2, stocks, win_size, stdev): 
        companies = stocks.split(',')
        vs.plot_bollinger(dict2, companies, win_size, stdev)
     
     
    def macd(self):
        child = tk.Toplevel(self.master)
        stock_macd = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_macd = tk.Entry(child,font = self.text_font)
        stock_macd.pack(pady=5, padx=5)
        self.stock_macd.pack(pady=5, padx=5)
        
        fema = tk.Label(child,text="Please enter the length of the Fast EMA: ", font = self.text_font)
        self.fema = tk.Entry(child,font = self.text_font)
        fema.pack(pady=5, padx=5)
        self.fema.pack(pady=5, padx=5)
        
        sema = tk.Label(child,text="Please enter the length of the Slow EMA: ", font = self.text_font)
        self.sema = tk.Entry(child,font = self.text_font)
        sema.pack(pady=5, padx=5)
        self.sema.pack(pady=5, padx=5)
        
        smooth = tk.Label(child,text="Please enter the period of the Signal Line", font = self.text_font)
        self.smooth = tk.Entry(child,font = self.text_font)
        smooth.pack(pady=5, padx=5)
        self.smooth.pack(pady=5, padx=5)

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_macd(self.dict2, self.stock_macd.get(), self.fema.get(), self.sema.get(), self.smooth.get()))
        describe.pack(pady=10, padx=10)                 

    def get_macd(self, dict2, stocks, fema, sema, smooth): 
        companies = stocks.split(',')
        vs.plot_macd(dict2, companies, fema, sema, smooth)
    
     
    def rsi(self):
        child = tk.Toplevel(self.master)
        stock_rsi = tk.Label(child,text="For which stock do you wish to make your analysis: " + ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_rsi = tk.Entry(child,font = self.text_font)
        stock_rsi.pack(pady=5, padx=5)
        self.stock_rsi.pack(pady=5, padx=5)
        
        sma_win = tk.Label(child,text="Please select the Window Size: ", font = self.text_font)
        self.sma_win = tk.Entry(child,font = self.text_font)
        sma_win.pack(pady=5, padx=5)
        self.sma_win.pack(pady=5, padx=5)  

        describe = tk.Button(child,text="Plot stocks", width = 10, font = self.button_font, command = lambda: self.get_rsi(self.dict2, self.stock_rsi.get(), self.sma_win.get()))
        describe.pack(pady=10, padx=10)                 

    def get_rsi(self, dict2, stocks, win_size): 
        companies = stocks.split(',')
        vs.plot_rsi(dict2, companies, win_size)
   

    def auto_c(self):
        child = tk.Toplevel(self.master)
        stock_raw = tk.Label(child,text="For which company do you wish to make your analysis: "+ ', '.join(list(self.dict.keys())), font = self.text_font)
        self.stock_raw = tk.Entry(child,font = self.text_font)
        stock_raw.pack(pady=5, padx=5)
        self.stock_raw.pack(pady=5, padx=5)       
        
        describe = tk.Button(child,text="Plot Stock", width = 10, font = self.button_font, command = lambda: self.get_auto_c(self.dict2, self.stock_raw.get()))
        describe.pack(pady=10, padx=10)   
     
    def get_auto_c(self, dict2, company):       
        companies = company.split(',')
        vs.auto_correl(dict2, companies)


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
        self.dict2 = datef._mutate_date_(copy.deepcopy(self.dict))
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




















