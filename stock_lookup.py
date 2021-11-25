
"""Request commands based on the code found in the documentation for Alphavantage/ 
    Link: https://www.alphavantage.co/documentation/"""
    
import requests
import tkinter as tk

def req_list_symb(keywords, key):
    #Function that asks the user to input their key and a name
    #Returns a dictionary with a list of the companies 
    #with the most similar name
    if key == "":
        raise tk.messagebox.showerror("Error", "No key available")
    symbol_func = "SYMBOL_SEARCH"
    symbol_url = 'https://www.alphavantage.co/query?function={}&keywords={}&apikey={}'.format(
    symbol_func, keywords, key)
    req_symb = requests.get(symbol_url)
    comp_stock = req_symb.json()
    return comp_stock


def comp_list(comp_stock):
    #Prints out the search results for the company symbols request
    if len(comp_stock['bestMatches']) > 0:
        for company in comp_stock['bestMatches']:
            print("Company Symbol : ", company['1. symbol'], "\n",  
              "Company Name : ", company['2. name'], "\n",
              "Stock Type : ", company['3. type'], "\n", 
              "Region : ", company['4. region'], "\n")
        print("If you want to look for a stock info, please use the company symbol")
    else:
        print("No companies were found. Try again")
    

def symb_names(keywords, key):
    #Looking up a company's symbol
    comp_stock = req_list_symb(keywords, key)
    comp_list(comp_stock)
    
    
    
    





















