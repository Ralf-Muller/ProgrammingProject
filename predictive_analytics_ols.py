# Importing all the relevant libraries for the OLS Regression
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression # We use the Linear Regression from Sklearn
import seaborn as sns # We decided to import seaborn to update the graphs and plots from matplotlib
from datetime import datetime
import stk_requestF as stkr
import tkinter as tk
import dataframe_image as dfi

sns.set()

''' Generate a simple OLS regression model for one data set
    The basis for the OLS model was obtained through the knowledge acquired in the Udemy Course:
    The Data Science Course 2021: Complete Data Science Bootcamp'''
def sk_simple_OLS(stocks, company, t_size, size):
    # Generating the two Linear Models for the Test and Plots
    inputs, targets, x_train, x_test, y_train, y_test= gen_model(stocks, company, t_size, size)
    reg, predicted_v = model_OLS(inputs, x_train, y_train)
    month = get_month(stocks, company[0])
    
    # Generate the Plots and output from the linear regression model considering if we have 1 or two stocks
    if size == 1:
        plot_OLS1(inputs, targets, predicted_v, reg, company[0], month)
    elif size == 2:
        plot_OLS2(inputs, targets, predicted_v, reg, company[0], company[1])
    plot_yhat_v_y(x_train, y_train, reg)
    
    # Create the variables to Return to the user
    test_result = sk_test_OLS(x_test, y_test, reg)
    test_styled = test_result.style.background_gradient()
    dfi.export(test_styled,"testtable.png")
    #model= sm.OLS(y_train,x_train).fit() # Overall analysis of the model
    # Create the variables to Return to the user
    RSME = sm.tools.eval_measures.rmse(predicted_v, targets, axis=0)
    R2 = reg.score(x_train,y_train)
    
    return RSME, R2, reg

# Generate the SKLearn OLS model to generate the graphs and obtain the results based on 1 or 2 stocks
def gen_model(stocks, company, t_size, size):
    # Import library to split the data into test and training values
    from sklearn.model_selection import train_test_split
    val_company(stocks,company)
    t_size = val_t_size(t_size)
    if size == 1:
        targets, inputs = get_price_date(stocks, company[0])
    elif size == 2:
        targets = stocks[company[0]]['5. adjusted close']
        inputs = stocks[company[1]]['5. adjusted close']
    inputs2 = sm.add_constant(inputs) # Transform the data to add the constant value
    x_train, x_test, y_train, y_test = train_test_split(inputs2, targets, test_size=t_size, random_state=365)
    return inputs, targets, x_train, x_test, y_train, y_test

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
    #plt.savefig('ols_regression.png')
    plt.show()

# Plotting the results from the regression model vs. the original scatterplot of stock1 vs. stock2
def plot_OLS2(inputs, targets, predicted_v, reg, company, company2):
    plt.scatter(inputs,targets)
    fig = plt.plot(inputs,predicted_v, lw=3, c='red', label ='OLS Regression')
    plt.title('Correlation Between Compan Stocks: ' + company + ' vs. ' + company2,fontsize = 14)
    plt.xlabel(company2, fontsize = 10)
    plt.ylabel(company, fontsize = 10)     
    plt.legend()
    #plt.savefig('ols2stocks.png')
    plt.show()

# Plot the values from the model vs. the real values
def plot_yhat_v_y(x_train, y_train, reg):
    y_hat = reg.predict(x_train)
    plt.scatter(y_train, y_hat)
    plt.title('Expected Results vs. Real Results',fontsize=18)
    #plt.xlabel('Real Values',fontsize=10)
    #plt.ylabel('Model Predictions',fontsize=10)
    #plt.savefig('y_train_v_y_hat.png')
    plt.show() 

# Function to validate if Symbol is in the downloaded dictionary
def val_company(stocks,companies):
    for company in companies:
        if company not in list(stocks):
            raise tk.messagebox.showerror("Error", "Stock not found in downloaded data. Did you use the correct symbol? Please try again")

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
def val_t_size(t_size):
    while True:
        try:
            t_size = float(t_size)
            if t_size > 1 or t_size <=0:
                raise tk.messagebox.showerror("Error", "Please enter a number between 0 and 1")
        except ValueError:
            raise tk.messagebox.showerror("Error", "Please enter a number for your Test Size")
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
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    test_table.sort_values(by=['Difference%'])
    return test_table 


# This function returns the predicted values and the graphs required for Predictive Analytics
def sk_predval_OLS(stocks, companies, t_size, date, size = 1):
    RSME, R2, reg = sk_simple_OLS(stocks, companies, t_size, size)
    stkr.validate(date,date)
    coef = datetime.strptime(date, "%Y-%m-%d").timestamp()
    pred_test = reg.intercept_+reg.coef_[1]*coef
    str_ols = "The predicted value for " + str(date) + " is: " + str(round(pred_test,2)) + \
        "\nThe coefficient of determination of the model is: " + str(round(R2,2))+\
        "\nThe RSME for the model is: " + str(round(RSME,2))    
    return str_ols



# This function returns the correlation between two stocks
def OLS_two_stocks(stocks, companies, t_size, size =2):
    RSME, R2, reg = sk_simple_OLS(stocks, companies, t_size, size)
    ols2_str = "The coefficient of correlation between stocks is: " + str(round(R2,2)) +"\nThe RSME for the model is: "+str(round(RSME,2))
    return ols2_str