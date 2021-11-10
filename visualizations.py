# Function to get the window for the data visualization
def get_window():
    win_size = int(input('Please Choose a Window Size for your moving average: '))
    return win_size

# Returns the Raw Time Series of the Selected Stock
def raw_time_series(stocks):
    company = get_company(stocks)
    price = stocks[company]['5. adjusted close']
    date = stocks[company]['date']
    plt.scatter(date,price)
    plt.title('Raw Time Series '+ company,fontsize=18)
    plt.xlabel('Time in Seconds', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.show()
#raw_time_series(stock_dict2)

# Returns the trend line for the data series
def plot_trend_line(stocks):
    inputs, targets, x_train, x_test, y_train, y_test = gen_model(stocks)
    reg, predicted_v = model_OLS(inputs, x_train, y_train)
    plot_OLS(inputs, targets, predicted_v, reg)
#plot_trend_line(stock_dict2)

# Plot Moving Averages for Stocks given a Window Time
def moving_averages(stocks):
    company = get_company(stocks)
    win_size = get_window()
    price = stocks[company]['5. adjusted close']
    sma = price.rolling(window =win_size).mean()
    std = price.rolling(window =win_size).std()
    return sma, std, company, win_size

def plot_sma(stocks):
    sma, std, company, win_size = moving_averages(stocks)
    plt.title('SMA '+ company,fontsize=18)
    plt.xlabel('Days', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.plot(stocks[company]['5. adjusted close'], label="Closing Prices")
    plt.plot(sma, label=str(win_size)+' Day SMA')
    plt.legend()
#plot_sma(stock_dict2)

# Plotting Bollinger Bands
def bollinger_band(stocks):
    sma, std, company, win_size = moving_averages(stocks)
    num_std = float(input('How many standard deviations away from the mean do you wish to calculate? '))
    upper_b = sma + std * num_std
    lower_b = sma - std * num_std
    return upper_b , lower_b, company

def plot_bollinger(stocks):
    upper_b , lower_b, company = bollinger_band(stocks)
    plt.title('Bollinger Band '+ company,fontsize=18)
    plt.xlabel('Days', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.plot(stocks[company]['5. adjusted close'], label="Closing Prices")
    plt.plot(upper_b, label='Bollinger Up', c='g')
    plt.plot(lower_b, label='Bollinger Down', c='r')
    plt.legend()
    plt.show()
#plot_bollinger(stock_dict2)    

# Plot Weighted Moving Averages from Data Set
def wma(stocks):
    company = get_company(stocks)
    win_size = get_window()
    weights = np.array([(i+1)/sum(range(win_size+1)) for i in range(win_size)])
    stocks[company]['5. adjusted close'].rolling(window =win_size).apply(lambda x: np.sum(weights*x)).plot(label=company)
#wma(stock_dict2)

# Plot MACD of time series
# The code for MACD adapted for the project was obtained from https://medium.com/codex/algorithmic-trading-with-macd-in-python-1c2769a6ad1b
def obtain_macd(stocks):
    company = get_company(stocks)
    date = stocks[company]['date']
    price = stocks[company]['5. adjusted close']
    fema = float(input('Please enter the length of the fast EMA: '))
    sema = float(input('Please enter the length of the slow EMA: '))
    smooth = float(input('Please enter the period of the Signal line: '))
    fast = price.ewm(span = fema, adjust = False).mean()
    slow = price.ewm(span = sema, adjust = False).mean()
    macd = pd.DataFrame(fast - slow).rename(columns = {'5. adjusted close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [date, macd, signal, hist]
    macd_df = pd.concat(frames, join = 'inner', axis = 1)
    return macd_df, company

def plot_macd(stocks):
    macd_df, company = obtain_macd(stocks)
    price = stocks[company]['5. adjusted close']
    hist = macd_df['hist']
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)

    ax1.plot(price)
    ax2.plot(macd_df['macd'], color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(macd_df['signal'], color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(price)):
        if str(hist[i])[0] == '-':
            ax2.bar(price.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(price.index[i], hist[i], color = '#26a69a')

    plt.legend(loc = 'lower right')
#plot_macd(stock_dict2)

# Plot Relative Strength Index for the selected Stock
# The code was adapted to the program from https://tcoil.info/compute-rsi-for-stocks-with-python-relative-strength-index/
def obtain_rsi(stocks, company, date, price):
    win_size = get_window() 
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

def plot_rsi(stocks):
    company = get_company(stocks)
    date = stocks[company]['date']
    price = stocks[company]['5. adjusted close']  
    stocks[company]['rsi'] = obtain_rsi(stocks, company, date, price)
    plt.title('Relative Strength Index '+company,fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('RSI', fontsize = 10)
    plt.plot(date, stocks[company]['rsi'])
    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    plt.show()
#plot_rsi(stock_dict2)

def auto_correl(stocks):
    company = get_company(stocks)
    price = stocks[company]['5. adjusted close']
    graph = pd.plotting.autocorrelation_plot(price)
    plt.title('Autocorrelation Plot',fontsize=18)
    graph.plot()
    plt.show()
#auto_correl(stock_dict2)