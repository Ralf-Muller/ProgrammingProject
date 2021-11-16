import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def raw_time_series(stocks): 
    company1 = get_company(stocks)
    price1, date1 = get_price_date(stocks, company1)
    company2 = get_company(stocks)
    price2, date2 = get_price_date(stocks, company2)
    month = get_month(stocks, company1)
    plt.plot(month, price1)
    plt.plot(month, price2)
    plt.title('Raw Time Series '+ company1,fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Adj. Closing Price', fontsize = 10)
    plt.legend() # you need to create labels in each each plt.plot
    plt.show()
# Put company2 into second y-axis
raw_time_series(stock_dict2)
