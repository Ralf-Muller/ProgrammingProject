#Generates a floating point value for each date in the stock data sets selected
from datetime import datetime
import pandas as pd

def _mutate_date_(stocks):
    # Iterate over the different companies that the client has selected
    for company in stocks: 
        stocks[company].reset_index(inplace=True)
        temp_time = []
        for index,day in enumerate(stocks[company]["index"]):
            dateAsString = day
            temp_time.append(datetime.strptime(
                    dateAsString, "%Y-%m-%d").timestamp())
            stocks[company]["index"][index] = datetime.strptime(
                    dateAsString, "%Y-%m-%d")
        stocks[company]["time"] = pd.to_numeric(temp_time, errors='coerce')
        stocks[company].rename(columns = {'index':'date'}, inplace = True)
    return stocks
