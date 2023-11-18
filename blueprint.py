import logging
import azure.functions as func
import pandas as pd
from io import BytesIO
import random
import yfinance as yf
import json
import requests


api_key = "a8dcb5acefdcb38357cf12102169abdc" # Enter your API key here
base_url = "http://api.openweathermap.org/data/2.5/weather?"



def get_weather_info(city_name):
    """
    A function to generate retrieve weather data

    :return:
    """
    url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(url)
    x = response.json()
    temperature = '----'
    pressure = '----'
    humidity = '----'
    weather_condition = '----'
    if x["cod"] != "404":
        y = x["main"]
        temperature = y["temp"]
        pressure = y["pressure"]
        humidity = y["humidity"]
        weather_condition = x["weather"][0]["description"]
    else:
        print(" City Not Found ")


    return temperature, humidity, weather_condition



currency_pairs = ["EURUSD=X", "GBPUSD=X", "EURGBP=X", "USDJPY=X"]


bp = func.Blueprint()

def get_exchange_rate(symbol):
    try:
        data = yf.download(symbol)
        last_price = data['Close'].iloc[-1]
        return last_price
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


# Fetch exchange rates
rates = {}
for pair in currency_pairs:
    rate = get_exchange_rate(pair)
    if rate is not None:
        rates[pair.split('=')[0]] = rate
    else:
        rates[pair] = '---'


@bp.route(route="rate_service", auth_level="anonymous")
def rate_service(req: func.HttpRequest) -> func.HttpResponse:
    global rates

    pair = req.params.get("pair") or "EURUSD"

    response = get_exchange_rate(pair+'=X') or '---'

    return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)


@bp.route(route="wheater_service", auth_level="anonymous")
def wheater_service(req: func.HttpRequest) -> func.HttpResponse:

    city = req.params.get("city") or "London"

    temperature, humidity, weather_condition = get_weather_info(city)

    response = {city: {
            'temperature': f'{temperature}°C',
            'humidity': f'{humidity}',
            'weather_condition': f'{weather_condition}',
        }
    }

    return func.HttpResponse(json.dumps(response), mimetype="application/json", status_code=200)








