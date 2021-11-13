# Function is designed to generate a floating point value for each date in the stock data sets selected
from datetime import datetime
import copy

def _mutate_date_(stocks):
    for company in stocks: # Iterate over the different companies that the client has selected
        stocks[company].reset_index(inplace=True)
        temp_time = []
        for index,day in enumerate(stocks[company]["index"]):
            dateAsString = day
            temp_time.append(datetime.strptime(dateAsString, "%Y-%m-%d").timestamp())
            stocks[company]["index"][index] = datetime.strptime(dateAsString, "%Y-%m-%d")
        stocks[company]["time"] = pd.to_numeric(temp_time, errors='coerce')
        stocks[company].rename(columns = {'index':'date'}, inplace = True)
    return stocks

stock_dict2 = _mutate_date_(copy.deepcopy(stock_dict))