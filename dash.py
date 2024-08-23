import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px
from datetime import datetime,date, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace 'file.csv' with the path to your CSV file
file_path = 'report.csv'

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path)

# Get the top 15 rows of data
bull = data['Bullish Stock'].head(15).values.tolist()
bear = data['Bearish Stock'].head(15).values.tolist()
list = bull + bear

#print(list)
st.title('Stock Dashboard')
#ticker = 'DRCSYSTEMS.NS'

ticker = st.sidebar.selectbox('Select Stock', list)
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End date')



data = yf.download('^NSEI',start = start_date, end=end_date, interval = "5m")
#data_1d = yf.download('RELIANCE.NS',start = (date.today() - timedelta(10)), end=date.today())
data.index = pd.to_datetime(data.index)
print(data['Adj Close'].dtype)
data['Adj Close'] = pd.to_numeric(data['Adj Close'], errors='coerce')
fig = px.line(data, x = data.index, y = data['Adj Close'], title = 'NIFTY 50')
st.plotly_chart(fig)

Pricing_data, Fundamental_data = st.tabs(["Pricing Data","Fundamental Ratio"]) 
with Pricing_data:
    st.header('Price Data')
    #stk = yf.download('RELIANCE.NS',start = (date.today() - timedelta(10)), end=date.today())
    stk = yf.download(ticker+'.NS',start = start_date, end=end_date, interval = "5m")
    print(stk)
    fig1 = px.line(stk, x = stk.index, y = stk['Adj Close'], title = ticker)
    st.plotly_chart(fig1)
    #st.write(data_1d)
    # Calculate daily returns
    #data_1d['Daily_Return'] = data_1d['Close'].pct_change()
    # Calculate volatility (standard deviation of daily returns)
    #volatility = data_1d['Daily_Return'].std()
    #print(data_1d['Daily_Return'].std())
    #st.write('Volatility is : ', volatility*100,'%')
    
#from alpha_vantage.fundamentaldata import FundamentalData
with Fundamental_data:
    # Set up the webdriver (you may need to download the appropriate webdriver for your browser)
    #company = input("Enter: ")
    url = "https://www.screener.in"
    driver = webdriver.Chrome()
    driver.get(url)
    elem = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div/div/input")
    elem.send_keys(ticker)
    time.sleep(2)
    elem = driver.find_elements(By.CLASS_NAME, "active")
    elem[1].click()
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    elem = wait.until(EC.presence_of_element_located((By.ID, "top-ratios")))
    data = elem.text

    lst = data.split("\n")
    print(lst)
    map = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}

    
    for k,v in map.items():
        st.write(k,"->",v)
        #print(k,"->",v)
    #print("\nDONE")
    driver.quit()
    

    
