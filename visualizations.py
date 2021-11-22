import matplotlib.pyplot as plt
import predictive_analytics_ols as stkols
import tkinter as tk
import numpy as np
import pandas as pd

# Function to get the window for the data visualization
def val_window(win_size):
    while True:
        try:
            win_size = abs(int(win_size))
        except ValueError:
            raise tk.messagebox.showerror("Error", "Please enter a number for your Window Size")
            continue
        break
    return win_size

# Get the Standard Deviation for the Bollinger Bands
def val_std(st_dev):
    while True:
        try:
            num_std = abs(float(st_dev))
        except ValueError:
            raise tk.messagebox.showerror("Error", "Please enter a number for your Standard Deviation")
            continue
        break
    return num_std

# Testing if the inputs for the MACD are numbers
def get_ema(emas):
    while True:
        try:
            ema = abs(float(emas))
        except ValueError:
            raise tk.messagebox.showerror("Error", "Please enter a number for your EMA and Signal Line")
            continue
        break
    return ema

#Function to obtain data for the MACD
def val_data_macd(fema, sema, smooth):
    still_ask = True
    while still_ask == True:
        fema = get_ema(fema)
        sema = get_ema(sema)
        if sema >= fema:
            raise tk.messagebox.showerror("Error",'Please enter a Fast EMA greater than the Slow EMA')
        else:
            still_ask = False
    smooth = get_ema(smooth)
    return fema, sema, smooth

# Returns the Raw Time Series of the Selected Stock
def raw_time_series(stocks, company): 
    #company = get_company(stocks)
    stkols.val_company(stocks, company)
    price, date = stkols.get_price_date(stocks, company[0])
    month = stkols.get_month(stocks, company[0])
    plt.plot(month, price)
    plt.title('Raw Time Series '+ company[0],fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    #plt.savefig('Raw_ts.png')

# Returns the trend line for the data series
def plot_trend_line(stocks, company, t_size, size = 1):
    stkols.val_company(stocks, company)    
    inputs, targets, x_train, x_test, y_train, y_test = stkols.gen_model(stocks, company, t_size, size)
    month = stkols.get_month(stocks, company[0])
    reg, predicted_v = stkols.model_OLS(inputs, x_train, y_train)
    stkols.plot_OLS1(inputs, targets, predicted_v, reg, company[0], month)

# Plot Moving Averages for Stocks given a Window Time
def moving_averages(stocks, company, win_size):
    price, date = stkols.get_price_date(stocks, company[0])
    sma = price.rolling(window =win_size).mean()
    std = price.rolling(window =win_size).std()
    return sma, std, price

def plot_sma(stocks, company, win_size):
    stkols.val_company(stocks, company)
    win_size = val_window(win_size)
    sma, std, price = moving_averages(stocks, company, win_size)
    month = stkols.get_month(stocks, company[0])
    plt.title('SMA '+ company[0],fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.plot(month, price, label="Closing Prices")
    plt.plot(month, sma, label=str(win_size)+' Day SMA')
    plt.legend()
    #plt.savefig('moving_averages.png')

# Plotting Bollinger Bands
def bollinger_band(stocks, company, win_size, stdev):
    stkols.val_company(stocks, company)
    win_size = val_window(win_size)
    num_std = val_std(stdev)
    sma, std, price = moving_averages(stocks, company, win_size)
    upper_b = sma + std * num_std
    lower_b = sma - std * num_std
    return upper_b , lower_b

def plot_bollinger(stocks, company, win_size, stdev):
    upper_b , lower_b = bollinger_band(stocks, company, win_size, stdev)
    month = stkols.get_month(stocks, company[0])
    plt.title('Bollinger Band '+ company[0],fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.plot(month, stocks[company[0]]['5. adjusted close'], label="Closing Prices")
    plt.plot(month, upper_b, label='Bollinger Up', c='g')
    plt.plot(month, lower_b, label='Bollinger Down', c='r')
    plt.legend()
    #plt.savefig('bollinger_bands.png')

# Plot Weighted Moving Averages from Data Set
def plot_wma(stocks, company, win_size):
    stkols.val_company(stocks, company)
    win_size = val_window(win_size)
    price, date = stkols.get_price_date(stocks, company[0])
    month = stkols.get_month(stocks, company[0])
    weights = np.array([(i+1)/sum(range(win_size+1)) for i in range(win_size)])
    plt.title('Weighted Moving Average '+ company[0],fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    wma = stocks[company[0]]['5. adjusted close'].rolling(window =win_size).apply(lambda x: np.sum(weights*x))
    plt.plot(month, price, label="Closing Prices")
    plt.plot(month, wma, label=str(win_size)+' Day WMA')
    plt.legend()
    #plt.savefig('wma.png')

# Plot MACD of time series
# The code for MACD adapted for the project was obtained from https://medium.com/codex/algorithmic-trading-with-macd-in-python-1c2769a6ad1b
def obtain_macd(stocks, company, fema, sema, smooth):
    stkols.val_company(stocks, company)
    fema, sema, smooth = val_data_macd(fema, sema, smooth)
    price, date = stkols.get_price_date(stocks, company[0])
    fast = price.ewm(span = fema, adjust = False).mean()
    slow = price.ewm(span = sema, adjust = False).mean()
    macd = pd.DataFrame(fast - slow).rename(columns = {'5. adjusted close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [date, macd, signal, hist]
    macd_df = pd.concat(frames, join = 'inner', axis = 1)
    return macd_df, price

def plot_macd(stocks, company, fema, sema, smooth):
    macd_df, price = obtain_macd(stocks, company, fema, sema, smooth)
    hist = macd_df['hist']
    plt.title('MACD '+ company[0],fontsize=18)
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
    plt.xlabel('Date', fontsize = 10)
    ax1.plot(price)
    ax2.plot(macd_df['macd'], color = 'y', linewidth = 1.5, label = 'MACD')
    ax2.plot(macd_df['signal'], color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(price)):
        if str(hist[i])[0] == '-':
            ax2.bar(price.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(price.index[i], hist[i], color = '#26a69a')

    plt.legend(loc = 'lower right')
    #plt.savefig('macd.png')

# Plot Relative Strength Index for the selected Stock
# The code was adapted to the program from https://tcoil.info/compute-rsi-for-stocks-with-python-relative-strength-index/
def obtain_rsi(stocks, company, win_size, date, price):
    change = price.diff(1).dropna() # The changes will be calculated on a daily basis
    gain = 0 * change
    gain[change > 0] = change[change > 0]
    loss = 0 * change
    loss[change < 0] = change[change < 0]
    gain_avg = gain.ewm(com=win_size-1, min_periods=win_size).mean()
    loss_avg = loss.ewm(com=win_size-1, min_periods=win_size).mean()
    rsn = gain_avg/loss_avg # RSN esquals average gain over period divided by average loss in period
    RSI = 100 - (100/(1+abs(rsn)))
    return RSI

def plot_rsi(stocks, company, win_size):
    stkols.val_company(stocks, company)
    win_size = val_window(win_size)
    price, date = stkols.get_price_date(stocks, company[0])
    month = stkols.get_month(stocks, company[0])
    stocks[company[0]]['rsi'] = obtain_rsi(stocks, company, win_size, date, price)
    plt.title('Relative Strength Index '+company[0],fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('RSI', fontsize = 10)
    plt.plot(month, stocks[company[0]]['rsi'])
    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5, color = 'red')
    plt.axhline(30, linestyle='--', color='grey')

    plt.axhline(70, linestyle='--', color='grey')
    plt.axhline(80, linestyle='--', alpha=0.5, color = 'red')
    plt.axhline(100, linestyle='--', alpha=0.1)
    #plt.savefig('rsi.png')

# Plot Autocorrelation from Stock
def auto_correl(stocks, company):
    stkols.val_company(stocks, company)
    price, date = stkols.get_price_date(stocks, company[0])
    graph = pd.plotting.autocorrelation_plot(price)
    plt.title('Autocorrelation Plot '+ company[0],fontsize=18)
    graph.plot()
    #plt.savefig('autocorrelation.png')
