

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

        #self.find = tk.Button(master, text="Find Company Symbol", command = self.scr_req_list_symb())
        #self.find.pack(pady=10)
            
    #def scr_req_list_symb(self):
        #Function that asks the user to input their key and a name
        #Returns a dictionary with a list of the companies 
        #with the most similar name
        key_q = tk.Label(text="Please enter Alphavantage key: ")
        self.key = tk.Entry()
        key_q.pack()
        self.key.pack()
        #self.key = self.key.get()
             
        keywords_q = tk.Label(text="Please enter company name: ")
        self.keywords = tk.Entry()
        keywords_q.pack()
        self.keywords.pack()
        #self.keywords = self.keywords.get()

        search = tk.Button(text="Search", command = lambda: self.symb_names(self.keywords.get(), self.key.get()))
        search.pack(pady=10)


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
        if len(comp_stock['bestMatches']) > 0:
            for company in comp_stock['bestMatches']:
                self.msg_window("Company Symbol : " + company['1. symbol'] + "\n" + 
              "Company Name : " + company['2. name'] + "\n" +
              "Stock Type : " + company['3. type'] + "\n" + 
              "Region : " + company['4. region'] + "\n")
        else:
            self.msg_window("No companies were found. Try again")
    

    def symb_names(self, keywords, key):
        #Looking up a company's symbol
        comp_stock = self.req_list_symb(keywords, key)
        self.comp_list(comp_stock)   
    
    #def comp_list(self, keywords, key):
    #Prints out the search results for the company symbols request
        #if len(comp_stock['bestMatches']) > 0:
           # for company in comp_stock['bestMatches']:
            #    self.msg_window("Company Symbol : " + company['1. symbol'] + "\n" +  
            #                "Company Name : " + company['2. name'] + "\n" +
           #                 "Stock Type : " + company['3. type'] + "\n" +
          #                  "Region : " + company['4. region'] + "\n")
        #else:
         #   self.msg_window("No companies were found. Try again")
        self.msg_window("This is what I have: {} {}".format(keywords, key))
            
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



