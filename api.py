import requests
from os import getenv

API_KEY = getenv("WEATHER_API_KEY")

def get_temperatura_cidade(cidade:str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}"
    
    request = requests.get(url).json()
    if request.get('main'):
        kelvin = request['main']['temp']
        temperatura_celsius = kelvin - 273.15
        return temperatura_celsius
    else:
        print(f"A cidade {cidade} não foi encontrada. Verifique o nome")
        return
