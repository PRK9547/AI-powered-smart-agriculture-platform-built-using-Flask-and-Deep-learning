import requests

API_KEY = "98a1aefce6dc031fb9f01c5712ef2e05"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    temperature = response["main"]["temp"]
    humidity = response["main"]["humidity"]
    rainfall = response.get("rain", {}).get("1h", 0)

    return temperature, humidity, rainfall
