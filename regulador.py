import db
from api import get_temperatura_cidade
from entities import Ambiente, ArCondicionado

ambientes = db.get_ambientes()
if ambientes is None:
    print("Houve um erro ao buscar pelos ambientes no Banco de Dados")
    exit(1)

for ambiente in ambientes:
    print(f"Verificando Ambiente {ambiente.nome}")
    print(f"Temperatura do ambiente: {ambiente.getTemperaturaSala()} °C")
    temp_cidade = get_temperatura_cidade(ambiente.cidade)
    if temp_cidade is not None:
        print(f"Temperatura Externa: {temp_cidade} °C")
    print(f"Temperatura Desejada: {ambiente.temperaturaDesejada} °C")
    
def regular_temp(ambiente:Ambiente, temp_externa:float):
    #Considerando que os ares-condicionados foram corretamente dimencionados no ambiente com uma capacidade máxima capaz de suportar um caso extremo de 38 °C 
    #Vamos calcular a capacidade em que os ares devem trabalhar a partir deste valor 
    carga_termica_ambiente_maxima = ambiente.getCargaTermica()
    diferenca_temperatura_maxima = 38.0 - ambiente.temperaturaDesejada
    diferenca_temperatura_atual = ambiente.getTemperaturaSala() - ambiente.temperaturaDesejada
    if int(diferenca_temperatura_atual) == 0:
        print("parei aqui")
    carga_termica_ambiente_atual = (carga_termica_ambiente_maxima * diferenca_temperatura_atual) / diferenca_temperatura_maxima




