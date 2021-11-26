"""References:
Copy and differences, astype  from Pandas documentation
ACF and PACF functions from the Statsmodels documentation
Help with correlograms from: 
https://www.statsmodels.org/dev/examples/notebooks/generated/tsa_arma_0.html

Actual ARIMA 
https://www.machinelearningplus.com/time-series/\
arima-model-time-series-forecasting-python/

ARIMA PLOT HELP: 
https://docs.w3cub.com/statsmodels/generated/\
statsmodels.tsa.arima_model.arimaresults.plot_predict

Code for exponential and Holt methods 
https://www.statsmodels.org/dev/examples/notebooks/generated/\
exponential_smoothing.html?highlight=exponential%20smoothing#\
Simple-Exponential-Smoothing

Some others: 
https://stackoverflow.com/questions/58510659/\
error-valuewarning-a-date-index-has-been-provided-but-it-has-no-associated-fr/\
58511282
https://stackoverflow.com/questions/29394730/\
converting-periodindex-to-datetimeindex
"""


import stk_requestF as sr
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA  
import statsmodels.tsa.api as sm_tsa
import datetime
import tkinter as tk
from stk_requestF import validate



def series_extract(stock, stock_dict):
    #Extracts a series from the dataframe
    try:
        cur_seri = pd.Series(stock_dict[stock]["5. adjusted close"].copy())
        cur_seri.index = pd.to_datetime(cur_seri.index).to_period("B")
    except KeyError:
        raise tk.messagebox.showerror("Error", 
              "Stock doesn't exist in the dictionary")
    return cur_seri


def correlogram(stock_dict, stock, diff, lags):
    #Creates the graphs for ACF and PACF based on user input
    cur_seri = series_extract(stock, stock_dict) 
    comb = plt.figure()  
    if diff == "1":
        try:
            first_diff = cur_seri.diff()
            ax1 = comb.add_subplot(211)
            comb = sm.graphics.tsa.plot_acf(first_diff.dropna(), lags = lags,
                                            ax = ax1)
            ax2 = comb.add_subplot(212)
            comb = sm.graphics.tsa.plot_pacf(first_diff.dropna(), lags = lags,
                                             ax = ax2)
        except IndexError:
             raise tk.messagebox.showerror("Error",
                                           "Don't put 0 as a lag level")
        except ValueError:
             raise tk.messagebox.showerror("Error",
           "Did you write a number above the possible lag limit or a letter?.")
    else:
        try:
            ax1 = comb.add_subplot(211)
            comb = sm.graphics.tsa.plot_acf(cur_seri.dropna(), lags = lags,
                                            ax = ax1)
            ax2 = comb.add_subplot(212)
            comb = sm.graphics.tsa.plot_pacf(cur_seri.dropna(), lags = lags,
                                             ax = ax2)
        except IndexError:
            raise tk.messagebox.showerror("Error", 
                  "Don't put 0 as a lag level")
        except ValueError:
            raise tk.messagebox.showerror("Error", 
          "Did you write a number above the possible lag limit or a letter?.")


def make_arima(stock_dict, stock, order_p, order_dif, 
               order_q, pred_days, start_date):
    #Function for creating ARIMA
    validate(start_date, start_date)
    cur_seri = series_extract(stock, stock_dict)
    try:
        order_p = int(order_p)
        order_dif = int(order_dif)
        order_q = int(order_q)
        pred_days = int(pred_days)
    except:
        raise tk.messagebox.showerror("Error", 
              "Non-numerical value in order or days")
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    model = ARIMA(cur_seri.dropna(), order = (order_p, order_dif, order_q)) 
    try:
        res = model.fit()
    except ValueError:
        raise tk.messagebox.showerror("Error", "Not possible to produce ARIMA. Increase order d")
    results = res.summary()
    fig, ax = plt.subplots()
    try:
        fig = res.plot_predict(start = start_date, 
               end =  cur_seri.index[-1] + pred_days, dynamic = False, 
               ax = ax, plot_insample = False)
    except KeyError:
        raise tk.messagebox.showerror("Error", 
                      "Start Date is lower than the earliest date available")
    except ValueError:
        raise tk.messagebox.showerror("Error", 
                          "Start Date is above the latest date available.")
    return results


def co_integration(stock_dict, stock1, stock2):
    #Function for cointegration test
    cur_seri1 = series_extract(stock1, stock_dict) 
    cur_seri2 = series_extract(stock2, stock_dict)
    t_stat, p_val, crit_v = sm.tsa.stattools.coint(cur_seri1, cur_seri2)
    coint_string = "Results for the cointegration test : \n \
          T-statistic : {}   \n   \
          P-Value : {}   \n \
          Critical Values at: \n  \
          1% = {}   \n  \
          5% = {}   \n  \
          10% = {} \n \
          Null Hypothesis: The two series are cointegrated".format(
          t_stat, p_val, crit_v[0], crit_v[1], crit_v[2])
    return coint_string

 
#Functions for creating exponential models    

def valid_list(char):
    return int(char) in [0,1,2,3,4]

def date_processes(cur_seri, start_date, end_date):
    validate(start_date, end_date)
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    if start_date <= cur_seri.index[0].to_timestamp():
        raise tk.messagebox.showerror("Error", 
                              "Date earlier than the first date available")
    if end_date <= cur_seri.index[-1].to_timestamp():
        raise tk.messagebox.showerror("Error", 
                              "Date earlier than the last date available")
    diff_date_d = end_date-start_date
    diff_date = diff_date_d.days
    sr.date_order(start_date, end_date)
    return start_date, end_date, diff_date

def model_creation(cur_seri, smooth, damp, diff_date):
    fit1 = sm_tsa.SimpleExpSmoothing(cur_seri).fit(
            smoothing_level = smooth, optimized = False)
    fcast1 = fit1.forecast(diff_date).rename("SES")
    fit2 = sm_tsa.Holt(cur_seri).fit()
    fcast2 = fit2.forecast(diff_date).rename("Holt's")
    fit3 = sm_tsa.Holt(cur_seri, exponential=True).fit()
    fcast3 = fit3.forecast(diff_date).rename("Exponential")
    fit4 = sm_tsa.Holt(cur_seri, damped =True).fit(
    damping_slope= damp)
    fcast4 = fit4.forecast(diff_date).rename("Additive Damped")
    fit5 = sm_tsa.Holt(
            cur_seri, exponential=True, damped =True).fit()
    fcast5 = fit5.forecast(diff_date).rename("Multiplicative Damped")
    fit_list = [fit1, fit2, fit3, fit4, fit5]
    fcast_list = [fcast1, fcast2, fcast3, fcast4, fcast5]
    fit_and_fcast = list(zip(fit_list, fcast_list))
    return fit_and_fcast
    
def plotter_smooth(start_date, end_date, fit_and_fcast, 
                   cur_seri, ax, user_choice):
    color = ["red", "green", "blue", "cyan", "magenta"]
    try:
        user_list =  set(map(lambda x : int(x), 
                             filter(valid_list, user_choice)))
    except ValueError:
        raise tk.messagebox.showerror("Error", 
                  "You wrote a non-numerical character in smoothing options")  
    for i in user_list:
        fit_and_fcast[i][0].fittedvalues[start_date:end_date].plot(ax=ax,
                     color = color[i])
        if end_date > cur_seri.index[-1].to_timestamp() :
            fit_and_fcast[i][1].plot(ax=ax, color= color[i], legend=True)

def exponential_graphs(stock_dict, stock, start_date, end_date, smooth,
                       damp, user_choice):
    cur_seri = series_extract(stock, stock_dict)
    start_date, end_date, diff_date = date_processes(cur_seri, start_date,
                                                     end_date)
    try:
        smooth = float(smooth)
        damp = float(damp)
    except:
        raise tk.messagebox.showerror("Error", 
          "You wrote a non-numerical character in smoothing and damping options") 
    fit_and_fcast = model_creation(cur_seri, smooth, damp, diff_date)
    ax = cur_seri[start_date:end_date].plot(color="black", marker="o", 
                 figsize=(12, 8))
    plotter_smooth(start_date, end_date, fit_and_fcast, cur_seri, 
                   ax, user_choice)
    ax.set_ylabel("Smoothing Models")

    
