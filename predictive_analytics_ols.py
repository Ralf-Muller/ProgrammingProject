# Importing all the relevant libraries for the OLS Regression
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression # We use the Linear Regression from Sklearn
import seaborn as sns # We decided to import seaborn to update the graphs and plots from matplotlib
from datetime import datetime
import copy # Generate deepcopies of our dataset to run the model each time
sns.set()

''' Generate a simple OLS regression model for one data set
    The basis for the OLS model was obtained through the knowledge acquired in the Udemy Course:
    The Data Science Course 2021: Complete Data Science Bootcamp'''
def sk_simple_OLS(stocks, size):
    # Generating the two Linear Models for the Test and Plots
    inputs, targets, x_train, x_test, y_train, y_test, company, company2 = gen_model(stocks, size)
    reg, predicted_v = model_OLS(inputs, x_train, y_train)
    month = get_month(stocks, company)
    
    # Generate the Plots and output from the linear regression model considering if we have 1 or two stocks
    test_result = sk_test_OLS(x_test, y_test, reg)
    if size == 1:
        plot_OLS1(inputs, targets, predicted_v, reg, company, month)
    elif size == 2:
        plot_OLS2(inputs, targets, predicted_v, reg, company, company2)
    plot_yhat_v_y(x_train, y_train, reg)
    
    # Create the variables to Return to the user
    model= sm.OLS(y_train,x_train).fit()
    RSME = sm.tools.eval_measures.rmse(predicted_v, targets, axis=0)
    R2 = reg.score(x_train,y_train)
    # print(model.summary()) # Show the user all the information regarding the data
    # print(test_result) # Show the user how the model performed on the test data
    
    return RSME, R2, reg

''' This will return the results table from the OLS
    model, test_results, RSME = sk_simple_OLS(stock_dict2)
    model.summary() # Get a summary from the OLS Model
    print(test_results) # Get a table with the results from the model applied to Test Data'''


# Generate the SKLearn OLS model to generate the graphs and obtain the results based on 1 or 2 stocks
def gen_model(stocks, size):
    # Import library to split the data into test and training values
    from sklearn.model_selection import train_test_split
    t_size = get_t_size()
    while t_size > 1 or t_size <=0:
        t_size = float(input("Please select the a valid number between 0 and 1: "))
    company = get_company(stocks)
    if size == 1:
        targets, inputs = get_price_date(stocks, company)
        company2 = 0
    elif size == 2:
        company2 = input('To which stock do you wish to compare '+ company + ': \n' + ', '.join(list(stocks))
 + '? ')
        targets = stocks[company]['5. adjusted close']
        inputs = stocks[company2]['5. adjusted close']
    inputs2 = sm.add_constant(inputs) # Transform the data to add the constant value
    x_train, x_test, y_train, y_test = train_test_split(inputs2, targets, test_size=t_size, random_state=365)
    return inputs, targets, x_train, x_test, y_train, y_test, company, company2

# Generate the Basic Statsmodels OLS to generate the graphs and obtain the results
def model_OLS(inputs, x_train, y_train):
    reg = LinearRegression()
    reg.fit(x_train,y_train)
    predicted_v = inputs*reg.coef_[1]+reg.intercept_
    return reg, predicted_v

# Plotting the results from the regression model vs. the original scatterplot of date vs. price
def plot_OLS1(inputs, targets, predicted_v, reg, company, month):
    plt.scatter(month,targets)
    fig = plt.plot(month,predicted_v, lw=3, c='red', label ='OLS Regression')
    plt.title('Trend Line ' + company,fontsize=18)
    plt.xlabel('Date', fontsize = 10)
    plt.ylabel('Price', fontsize = 10)
    plt.legend()
    plt.show()

    
# Plotting the results from the regression model vs. the original scatterplot of stock1 vs. stock2
def plot_OLS2(inputs, targets, predicted_v, reg, company, company2):
    plt.scatter(inputs,targets)
    fig = plt.plot(inputs,predicted_v, lw=3, c='red', label ='OLS Regression')
    plt.title('Correlation Between Compan Stocks: ' + company + ' vs. ' + company2,fontsize = 14)
    plt.xlabel(company2, fontsize = 10)
    plt.ylabel(company, fontsize = 10)     
    plt.legend()
    plt.show()
    
# Plot the values from the model vs. the real values
def plot_yhat_v_y(x_train, y_train, reg):
    y_hat = reg.predict(x_train)
    plt.scatter(y_train, y_hat)
    plt.title('Expected Results vs. Real Results',fontsize=18)
    plt.xlabel('Real Values',fontsize=10)
    plt.ylabel('Model Predictions',fontsize=10)
    plt.show() 

# Get the company that the user will be working on while searching for the company in downloaded data
def get_company(stocks):
    company = input("For which company do you wish to make your analysis: \n" + ', '.join(list(stocks))
 + '? ')
    while company not in list(stocks):
        company = input("Please enter a valid stock that has been downloaded: \n" + ', '.join(list(stocks))+': ')
    return company

#Function to obtain the date & prices for each graph
def get_price_date(stocks, company):
    price = stocks[company]['5. adjusted close']
    date = stocks[company]['time']
    return price, date

# Obtain the datetime format data to plot each of the graphs
def get_month(stocks, company):
    month = stocks[company]['date']
    return month

# Obtain the test size for the regression model
def get_t_size():
    while True:
        try:
            t_size = float(input("Please select the Test Size as a decimal point: "))
        except ValueError:
            print('Your input is not a number')
            continue
        break
    return t_size

# This function is designed to test the model to new test data to guarantee the accuracy of the prediction
def sk_test_OLS(x_test, y_test, reg):
    pred_test = reg.predict(x_test) # Generate the prediction for the test data
    test_table = pd.DataFrame(pred_test, columns=['Prediction'])
    y_test = y_test.reset_index(drop=True) #Reset the index of y_test to match pred_test
    test_table['Target'] = y_test
    test_table['Residual'] = test_table['Target'] - test_table['Prediction'] # Calculate the residual
    test_table['Square Error'] = test_table['Residual'] * test_table['Residual'] # Calculate Square Error
    test_table['Difference%'] = np.absolute(test_table['Residual']/test_table['Target']*100)
    #pd.set_option('display.float_format', lambda x: '%.2f' % x)
    test_table.sort_values(by=['Difference%'])
    return test_table 


# This function returns the predicted values and the graphs required for Predictive Analytics
def sk_predval_OLS(stocks, size = 1):
    RSME, R2, reg = sk_simple_OLS(stocks, size)
    date = input("For which date do you wish to know the prediction? \nPlease use YYYY-MM-DD format: ")
    validate(date)
    coef = datetime.strptime(date, "%Y-%m-%d").timestamp()
    pred_test = reg.intercept_+reg.coef_[1]*coef
    return pred_test, date, RSME, R2
#pred_test, date, RSME, R2 = sk_predval_OLS(stock_dict2)
#print("The predicted value for ", date, " is: ", round(pred_test,2))
#print("The coefficient of determination of the model is: ", round(R2,2))
#print("The RSME for the model is: ", round(RSME,2))


# This function returns the correlation between two stocks
def OLS_two_stocks(stocks, size =2):
    RSME, R2, reg = sk_simple_OLS(stocks, size)
    print("The coefficient of correlation between stocks is: ", round(R2,2))
    print("The RSME for the model is: ", round(RSME,2))
#OLS_two_stocks(stock_dict2)
