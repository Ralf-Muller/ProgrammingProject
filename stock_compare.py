
import matplotlib.pyplot as plt
import seaborn as sns


sns.set()

#Function to obtain the prices for each graph
def get_price(stocks, company):
    price = stocks[company]['5. adjusted close']
    return price

# Obtain the datetime format data to plot each of the graphs
def get_day(stocks, company):
    day = stocks[company]['5. adjusted close'].index[:]
    return day

def compare_stk(stocks, company1, company2): 
    #Function to compare two stocks
    price1 = get_price(stocks, company1)
    price2 = get_price(stocks, company2)
    day = get_day(stocks, company1)
    fig, ax = plt.subplots()
    ax.plot(day, price1, label = company1)
    ax.plot(day, price2, label = company2)
    ax.set_xticklabels(day, rotation = 45)
    ax.xaxis.set_major_locator(plt.MaxNLocator(12))
    ax.set_title('Stock price comparision', fontsize=18)
    ax.set_xlabel('Date', fontsize = 10)
    ax.set_ylabel('{} stock price'.format(company1), fontsize = 10)
    #https://matplotlib.org/stable/gallery/subplots_axes_and_figures/
    #secondary_axis.html
    secax = ax.secondary_yaxis('right')
    secax.set_ylabel('{} stock price'.format(company2), fontsize = 10)
    plt.legend()




