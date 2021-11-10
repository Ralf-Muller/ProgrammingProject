import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
from datetime import datetime
import copy
sns.set()

def sk_simple_OLS(stocks): # Generate a simple OLS regression model for one data set

    inputs, targets, x_train, x_test, y_train, y_test = gen_model(stocks)
    reg, predicted_v = model_OLS(inputs, x_train, y_train)

    test_result = sk_test_OLS(x_test, y_test, reg)
    plot_OLS(inputs, targets, predicted_v, reg)
    plot_yhat_v_y(x_train, y_train, reg)
    
    model= sm.OLS(y_train,x_train).fit()
    # print(model.summary()) # Show the user all the information regarding the data
    # print(test_result) # Show the user how the model performed on the test data
    RSME = sm.tools.eval_measures.rmse(predicted_v, targets, axis=0)
    R2 = reg.score(x_train,y_train)
    
    return RSME, R2, reg

def gen_model(stocks):
    # Import library to split the data into test and training values
    from sklearn.model_selection import train_test_split 
    t_size = float(input("Please select the Test Size as a decimal point: "))
    company = get_company(stocks)
    targets = stocks[company]['5. adjusted close']
    inputs = stocks[company]['date']
    inputs2 = sm.add_constant(inputs) # Transform the data to add the constant value
    x_train, x_test, y_train, y_test = train_test_split(inputs2, targets, test_size=t_size, random_state=365)
    return inputs, targets, x_train, x_test, y_train, y_test

def model_OLS(inputs, x_train, y_train):
    reg = LinearRegression()
    reg.fit(x_train,y_train)
    predicted_v = inputs*reg.coef_[1]+reg.intercept_
    return reg, predicted_v

def get_company(stocks):
    company = input("For which company do you wish to make your analysis? \n" + str(stocks.keys()))
    return company

# Plotting the results from the regression model vs. the original scatterplot of date vs. price
def plot_OLS(inputs, targets, predicted_v, reg):
    plt.scatter(inputs,targets)
    fig = plt.plot(inputs,predicted_v, lw=3, c='red', label ='OLS Regression')
    plt.title('Trend Line ' + company,fontsize=18)
    plt.xlabel('Time', fontsize = 10)
    plt.ylabel('Price', fontsize = 10)
    plt.show()

# Plot the values from the model vs. the real values
def plot_yhat_v_y(x_train, y_train, reg):
    y_hat = reg.predict(x_train)
    plt.scatter(y_train, y_hat)
    plt.title('Expected Results vs. Real Results',fontsize=18)
    plt.xlabel('Targets (y_train)',fontsize=10)
    plt.ylabel('Predictions (y_hat)',fontsize=10)
    plt.show() 

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

def sk_predval_OLS(stocks):
    RSME, R2, reg = sk_simple_OLS(stocks)
    date = input("For which date do you wish to know the prediction? \nPlease use YYYY-MM-DD format: ")
    coef = datetime.strptime(date, "%Y-%m-%d").timestamp()
    pred_test = reg.intercept_+reg.coef_[1]*coef
    return pred_test, date, RSME, R2
pred_test, date, RSME, R2 = sk_predval_OLS(stock_dict2)
print("The predicted value for ", date, " is: ", pred_test)
print("The coefficient of determination of the model is: ", R2)
print("The RSME for the model is: ", RSME)