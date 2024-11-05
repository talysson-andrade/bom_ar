import db
from api import get_temperatura_cidade
from entities import Ambiente
from time import sleep
import datetime

def main():
    while True:
        print(f"{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}")
        ambientes = db.get_ambientes()
        if ambientes is None:
            print("Houve um erro ao buscar pelos ambientes no Banco de Dados")
            exit(1)
        for ambiente in ambientes:
            print()
            print(f"Verificando Ambiente {ambiente.nome}")
            print(f"Temperatura do ambiente: {ambiente.getTemperaturaSala()} °C")
            temp_cidade = get_temperatura_cidade(ambiente.cidade)
            if temp_cidade is not None:
                print(f"Temperatura Externa: {temp_cidade} °C")
            print(f"Temperatura Desejada: {ambiente.temperaturaDesejada} °C")
            print("Regulando a Temperatura do ambiente...")
            regular_temp(ambiente, temp_cidade)
        sleep(30)
            
def regular_temp(ambiente:Ambiente, temp_externa:float):
    #Considerando que os ares-condicionados foram corretamente dimencionados no ambiente com uma capacidade máxima capaz de suportar um caso extremo de 38 °C 
    #Vamos calcular a capacidade em que os ares devem trabalhar a partir deste valor 
    carga_termica_ambiente_maxima = ambiente.getCargaTermica()
    diferenca_temperatura_maxima = 38.0 - ambiente.temperaturaDesejada
    temperatura_sala = ambiente.getTemperaturaSala()
    if temperatura_sala is None:
        #Caso não seja possível obter informações dos sensores dos ares, usa a temperatura externa
        temperatura_sala = temp_externa
    diferenca_temperatura_atual = ambiente.getTemperaturaSala() - ambiente.temperaturaDesejada
    if int(diferenca_temperatura_atual) <= 0:
        for ar in ambiente.ares_condicionados:
            if int(diferenca_temperatura_atual == 0):
                #Temperatura desejada atingida
                #Reduzindo o funcionamento dos ares pra menor consumo de energia
                ar.modoBaixoConsumo()
            else:
                #Temperatura mais baixa que o desejado
                #Desligando os ares
                ar.desligar()
        return
    carga_termica_ambiente_atual = (carga_termica_ambiente_maxima * diferenca_temperatura_atual) / diferenca_temperatura_maxima
    #Com o valor da carga termica necessária para regular a temperatura do ambiente 
    #Vamos dividir a carga entre os ar condicionados do ambiente
    capacidade_ar = carga_termica_ambiente_atual / len(ambiente.ares_condicionados)    
    for ar in ambiente.ares_condicionados:
        fator = ((float(capacidade_ar) * 100.0) / float(ar.capacidade_total)) / 100.0
        #Percentual da capacidade total do ar condicionado em que ele deve atuar
        if not ar.estaLigado:
            ar.ligar()
        ar.regularPotencia(fator)
    return

if __name__ == "__main__":
    main()
