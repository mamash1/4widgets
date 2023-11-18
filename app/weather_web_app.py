import streamlit as st
import requests, json

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

city_name = 'Limassol'
st.title(f"{city_name} Weather App") # Create a Streamlit web app


temperature, humidity, weather_condition = get_weather_info(city_name)
st.write(f"Temperature: {round(temperature-273.15, 2)}°C")
st.write(f"Humidity: {humidity}%")
st.write(f"Condition: {weather_condition}")


