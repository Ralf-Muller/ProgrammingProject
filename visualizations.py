# Function to get the window for the data visualization
def get_window():
    while True:
        try:
            win_size = abs(int(input('Please Choose a Window Size for your moving average: ')))
        except ValueError:
            print('Your input is not a number')
            continue
        break
    return win_size

# Get the Standard Deviation for the Bollinger Bands
def get_std():
    while True:
        try:
            num_std = abs(float(input('How many standard deviations away from the mean do you wish to calculate? ')))
        except ValueError:
            print('Your input is not a number')
            continue
        break
    return num_std

# Testing if the inputs for the MACD are numbers
def get_ema(emas):
    while True:
        try:
            ema = abs(float(input('Please enter the length of the {}: '.format(emas))))
        except ValueError:
            print('Your input is not a number')
            continue
        break
    return ema

#Function to obtain data for the MACD
def get_data_macd():
    still_ask = True
    while still_ask == True:
        fema = get_ema("fast EMA")
        sema = get_ema("slow EMA")
        if sema >= fema:
            print('Please enter a fast EMA greater than the slow EMA')
        else:
            still_ask = False
    smooth = get_ema("the period of the Signal line")
    return fema, sema, smooth

# Returns the Raw Time Series of the Selected Stock
def raw_time_series(stocks): 
    company = get_company(stocks)
    price, date = get_price_date(stocks, company)
    month = get_month(stocks, company)
    plt.plot(month, price)
    plt.title('Raw Time Series '+ company,fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.show()
#raw_time_series(stock_dict2)

# Returns the trend line for the data series
def plot_trend_line(stocks):
    inputs, targets, x_train, x_test, y_train, y_test, company, company2 = gen_model(stocks, size=1)
    month = get_month(stocks, company)
    reg, predicted_v = model_OLS(inputs, x_train, y_train)
    plot_OLS1(inputs, targets, predicted_v, reg, company, month)
#plot_trend_line(stock_dict2)

# Plot Moving Averages for Stocks given a Window Time
def moving_averages(stocks):
    company = get_company(stocks)
    win_size = get_window()
    price, date = get_price_date(stocks, company)
    sma = price.rolling(window =win_size).mean()
    std = price.rolling(window =win_size).std()
    return sma, std, company, win_size, price

def plot_sma(stocks):
    sma, std, company, win_size, price = moving_averages(stocks)
    month = get_month(stocks, company)
    plt.title('SMA '+ company,fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.plot(month, price, label="Closing Prices")
    plt.plot(month, sma, label=str(win_size)+' Day SMA')
    plt.legend()
#plot_sma(stock_dict2)

# Plotting Bollinger Bands
def bollinger_band(stocks):
    sma, std, company, win_size, price = moving_averages(stocks)
    num_std = get_std()
    upper_b = sma + std * num_std
    lower_b = sma - std * num_std
    return upper_b , lower_b, company

def plot_bollinger(stocks):
    upper_b , lower_b, company = bollinger_band(stocks)
    month = get_month(stocks, company)
    plt.title('Bollinger Band '+ company,fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.plot(month, stocks[company]['5. adjusted close'], label="Closing Prices")
    plt.plot(month, upper_b, label='Bollinger Up', c='g')
    plt.plot(month, lower_b, label='Bollinger Down', c='r')
    plt.legend()
    plt.show()
#plot_bollinger(stock_dict2)    

# Plot Weighted Moving Averages from Data Set
def wma(stocks):
    company = get_company(stocks)
    win_size = get_window()
    price, date = get_price_date(stocks, company)
    month = get_month(stocks, company)
    weights = np.array([(i+1)/sum(range(win_size+1)) for i in range(win_size)])
    plt.title('Weighted Moving Average '+ company,fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    wma = stocks[company]['5. adjusted close'].rolling(window =win_size).apply(lambda x: np.sum(weights*x))
    plt.plot(month, price, label="Closing Prices")
    plt.plot(month, wma, label=str(win_size)+' Day WMA')
    plt.legend()
    plt.show()
#wma(stock_dict2)

# Plot MACD of time series
# The code for MACD adapted for the project was obtained from https://medium.com/codex/algorithmic-trading-with-macd-in-python-1c2769a6ad1b
def obtain_macd(stocks):
    company = get_company(stocks)
    price, date = get_price_date(stocks, company)
    fema, sema, smooth = get_data_macd()
    fast = price.ewm(span = fema, adjust = False).mean()
    slow = price.ewm(span = sema, adjust = False).mean()
    macd = pd.DataFrame(fast - slow).rename(columns = {'5. adjusted close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [date, macd, signal, hist]
    macd_df = pd.concat(frames, join = 'inner', axis = 1)
    return macd_df, company, price

def plot_macd(stocks):
    macd_df, company, price = obtain_macd(stocks)
    hist = macd_df['hist']
    plt.title('MACD '+ company,fontsize=18)
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
    price, date = get_price_date(stocks, company)
    month = get_month(stocks, company)
    stocks[company]['rsi'] = obtain_rsi(stocks, company, date, price)
    plt.title('Relative Strength Index '+company,fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('RSI', fontsize = 10)
    plt.plot(month, stocks[company]['rsi'])
    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(20, linestyle='--', alpha=0.5, color = 'red')
    plt.axhline(30, linestyle='--', color='grey')

    plt.axhline(70, linestyle='--', color='grey')
    plt.axhline(80, linestyle='--', alpha=0.5, color = 'red')
    plt.axhline(100, linestyle='--', alpha=0.1)
    plt.show()
#plot_rsi(stock_dict2)

def auto_correl(stocks):
    company = get_company(stocks)
    price, date = get_price_date(stocks, company)
    graph = pd.plotting.autocorrelation_plot(price)
    plt.title('Autocorrelation Plot '+ company,fontsize=18)
    graph.plot()
    plt.show()
#auto_correl(stock_dict2)