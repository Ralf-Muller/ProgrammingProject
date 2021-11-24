import stk_requestF as sr
import matplotlib.pyplot as plt
import seaborn as sns
#import pandas as pd

sns.set()
#key: 7QJ0OD6RU5IEVRO4

def compare_stk(stocks, company1, company2): 
    print('\nPlease give me two campany to analyse their historical adj. price.')
    #company1 = get_company(stocks)
    price1 = get_price(stocks, company1)
    #company2 = get_company(stocks)
    price2 = get_price(stocks, company2)
    day = get_day(stocks, company1)
    
    fig, ax = plt.subplots()
    ax.plot(day, price1, label = company1)
    ax.plot(day, price2, label = company2)
    ax.set_xticklabels(day, rotation = 45)
    ax.set_title('Stock price comparision', fontsize=18)
    ax.set_xlabel('Date', fontsize = 10)
    ax.set_ylabel('{} stock price'.format(company1), fontsize = 10)
    
    #https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html
    secax = ax.secondary_yaxis('right')
    secax.set_ylabel('{} stock price'.format(company2), fontsize = 10)# Put company2 into second y-axis
    plt.legend()#create labels in each each plt.plot
    plt.show()


# Get the company that the user will be working on while searching for the company in downloaded data
#From predictive ols
def get_company(stocks):
    company = input("For which company do you wish to make your analysis: \n" + ', '.join(list(stocks))+ '? ')
    while company not in list(stocks):
        company = input("Please enter a valid stock that has been downloaded: \n" + ', '.join(list(stocks))+': ')
    return company

#Function to obtain the prices for each graph
def get_price(stocks, company):
    price = stocks[company]['5. adjusted close']
    #date = stocks[company][0]
    return price#, date

# Obtain the datetime format data to plot each of the graphs
def get_day(stocks, company):
    day = stocks[company]['5. adjusted close'].index[:]
    #end_d = stocks[company]['5. adjusted close'].index[-1]
    #day = pd.date_range(start = start_d, end = end_d).tolist()
    return day

#key         = input("Please feed me your key for Alphavantage : ")
#stock       = input("Please feed me a company's stock name : ")
#start_date  = input("Please feed me the starting date in YYYY-MM-DD format: ")
#end_date    = input("Please feed me the ending date in YYYY-MM-DD format: ")

#s_dict = sr.req_to_frame(key, stock, start_date, end_date)

#compare_stk(s_dict)
