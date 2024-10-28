import requests

api_key = "f0298a14f006b00aa1ea4b9a2a5932a3"
cidade = input("Digite a cidade: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}"


request = requests.get(url).json()

if request.get('main'):
    # Obtenha a temperatura em Kelvin
    kelvin = request['main']['temp']

    # Converta para Celsius
    temperatura_celsius = kelvin - 273.15

    # Exiba apenas a temperatura
    print(f"A temperatura em {cidade} é: {temperatura_celsius:.2f} °C")
else:
    print("Cidade não encontrada. Verifique o nome e tente novamente.")