# To run this code:
# source venv/bin/activate
# streamlit run rates_web_app.py


import streamlit as st
import random
import yfinance as yf

def get_exchange_rate(symbol):
    try:
        data = yf.download(symbol)
        last_price = data['Close'].iloc[-1]
        return last_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Define the currency pairs
currency_pairs = ["EURUSD=X", "GBPUSD=X", "EURGBP=X", "USDJPY=X"]

# Fetch exchange rates
rates = {}
for pair in currency_pairs:
    rate = get_exchange_rate(pair)
    if rate is not None:
        rates[pair] = rate
    else:
        rates[pair] = '---'


st.title("Current Rates App") # Create a Streamlit web app

for pair, rate in rates.items():
    st.write(f"{pair.split('=')[0]}: {round(get_exchange_rate(pair) or '----', 4)}")




