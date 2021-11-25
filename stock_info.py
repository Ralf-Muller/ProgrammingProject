
import requests
import numpy as np
import statistics
import tkinter as tk


def get_overview(stock, key):
    #Function for requesting a company overview
    url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'.format(stock, key)
    r = requests.get(url)
    info = r.json()
    if "Symbol" not in info:
        raise tk.messagebox.showerror("Error", 
              "Stock not found in Alphavantage. Did you use the correct symbol? Please try again")
    str_ov = "Symbol:  {}\n\
            Name:  {}\n\
            Country:  {}\n\
            Sector:  {}\n\
            Industry:  {}".format(info["Symbol"], info["Name"], 
            info["Country"], info["Sector"], info["Industry"])
    return str_ov


def get_description(s_dict, stock):
    #Function for getting a company basic statistics
    values = s_dict[stock]['5. adjusted close']
    str_values = str('\n'+
          'Mean               : ' + "%.2f" % np.mean(values) + '\n' + 
          'Median             : ' + "%.2f" % np.median(values) + '\n' + 
          'Standard deviation :' + "%.2f" % statistics.stdev(values) + '\n' +
          'Variance           : ' + "%.2f" % statistics.variance(values) + 
          '\n' + 'Range: from ' + "%.2f" % min(values) + ' to ' + 
          "%.2f" % max(values) + '\n' + 'Q1 Quartiles       : ' +
          "%.2f" % np.quantile(values, .25, interpolation='midpoint') + '\n' +
          'Q2 Quartiles       : ' + 
          "%.2f" % np.quantile(values, .50, interpolation='midpoint') + '\n' +
          ' Q3 Quartiles       : ' +
          "%.2f" % np.quantile(values, .75, interpolation='midpoint') + '\n'
                  )
    return values, str_values

