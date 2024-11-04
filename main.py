from time import sleep
import db
import os
from typing import List
from entities import Ambiente, ArCondicionado
from api import get_temperatura_cidade

ambientes = db.get_ambientes()
if ambientes is None:
    exit(1)

def listar_ambientes():
    if not ambientes:
        print("Nenhum ambiente foi registrado")
    print()
    for ambiente in ambientes:
        print(f"{ambientes.index(ambiente) + 1 }. {ambiente.nome} - Temperatura Desejada: {ambiente.temperaturaDesejada} - Temperatura do Ambiente: {ambiente.getTemperaturaSala()} °C")
    print()

def menu():
    global ambientes
    limpar_cmd()
    print("        Sistema de Controle de Temperatura")
    print("_________________________________________________________")
    listar_ambientes()
    print("_________________________________________________________")
    print("Selecione uma das seguintes opções: ")
    print("Insira o valor do ambiente para ver mais configurações")
    print("(S)air    (N)ovo")
    resposta = input(">>> ")
    resposta = resposta.lower()
    
    match resposta:
        case "s":
            limpar_cmd()
            exit(0)
        case "n":
            print("")
            nome = input("Insira um nome para o novo Ambiente: \n>>> ")
            cidade = input("Insira a cidade em que esse Ambiente se localiza: \n>>> ")
            temperatura_desejada = float(input("Insira o valor da temperatura que deseja que este Ambiente se mantenha (ex: 23.5): \n>>> "))
            ambiente = Ambiente(nome, temperatura_desejada, cidade)
            db.insert_ambiente(ambiente)
            sleep(1)
            ambientes.clear()
            ambientes = db.get_ambientes() # Renova a lista de Ambientes
            menu()

        case _:
            if resposta.isdigit():
                index = int(resposta) - 1
                if index >= len(ambientes):
                    print("Número Inválido: O número deve corresponder a um dos ambientes listados")
                    sleep(1)
                    menu()
                conf_ambiente(index)
            else: 
                print("Resposta Invalída...")
                sleep(1)
                menu()

def conf_ambiente(index:int):
    global ambientes
    ambiente = ambientes[index]
    limpar_cmd()
    temp_cidade = round(get_temperatura_cidade(ambiente.cidade), 1)
    print("                      Ambiente")
    print("_________________________________________________________")
    print(f"Nome:  {ambiente.nome}")
    print(f"Temperatura Desejada: {ambiente.temperaturaDesejada}")
    print(f"Localização: {ambiente.cidade}   -->   {temp_cidade} °C")
    print()
    if not ambiente.ares_condicionados:
        print("Nenhum Ar-condicionado foi adicionado a este ambiente")
    if ambiente.ares_condicionados:
        print("     Ares-condicionados:")
        for ar in ambiente.ares_condicionados:
            status = "OFF"
            if ar.estaLigado:
                status = "ON"
            print(f"        {ambiente.ares_condicionados.index(ar) + 1}. {ar.nome} - {status}")
    
    print("_________________________________________________________")
    print("Selecione uma das seguintes opções ou insira o número do Ar-condicionado:")
    print("(A)dicionar Novo Ar-condicionado   |   Alterar (T)emperatura Desejada   |   (V)oltar")
    resposta = input(">>> ")
    resposta = resposta.lower()
    
    match resposta:
        case "a":
            nome = input("Insira um nome para o novo Ar-condicionado: \n>>> ")
            marca = input("Insira a marca do novo Ar-condicionado: \n>>> ")
            capacidade = int(input("Insira o valor da capacidade do novo Ar-condicionado (BTUs/h): \n>>> "))
            ar = ArCondicionado(nome, marca, capacidade)
            ambiente.adicionarArCondicionado(ar)
            db.insert_ar(ar, ambiente.id)
            sleep(1)
            conf_ambiente(index)
        case "t":
            print("")
            nova_temperatura = float(input("Insira o valor da nova temperatura desejada (ex: 24.5): \n>>> "))
            ambiente.temperaturaDesejada = nova_temperatura
            db.alterar_ambiente(ambiente)
            sleep(1)
            conf_ambiente(index)
        case "v":
            menu()
        case _:
            if resposta.isdigit():
                index_ar = int(resposta) - 1
                if index >= len(ambientes):
                    print("Número Inválido: O número deve corresponder a um dos ambientes listados")
                    sleep(1)
                    conf_ambiente(index)
                conf_arcondicionado(ambiente.ares_condicionados[index_ar], index)
            else: 
                print("Resposta Invalída...")
                sleep(1)
                conf_ambiente(index)

def conf_arcondicionado(ar_condicionado:ArCondicionado, index_ambiente:int):
    limpar_cmd()
    print("                   Ar-condicionado")
    print()
    print(f"Nome: {ar_condicionado.nome}")
    print(f"Marca: {ar_condicionado.marca}")
    if ar_condicionado.estaLigado:
        print("         Ligado")
        print(f"Sensor de Temperatura: {ar_condicionado.getTemperaturaSensor()}")
    else:
        print("         Desligado")

    print("_________________________________________________________")
    print("Selecione uma das seguintes opções: ")
    if ar_condicionado.estaLigado:
        print("(D)esligar   (A)lterar Nome    (V)oltar")
    else:
        print("(L)igar     (A)lterar Nome    (Voltar)")
    resposta = input(">>> ")
    resposta = resposta.lower()

    match resposta:
        case "d":
            ar_condicionado.desligar()
            sleep(1)
            conf_arcondicionado(ar_condicionado, index_ambiente)
        case "a":
            ar_condicionado.nome = input("Insira um novo nome para o Ar-condicionado:\n>>> ")
            db.alterar_ar_condicionado(ar_condicionado)
            sleep(1)
            conf_arcondicionado(ar_condicionado, index_ambiente)
        case "v":
            print(index_ambiente)
            sleep(3)
            conf_ambiente(index_ambiente)

def main():
    menu()

def limpar_cmd():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

if __name__ == "__main__":
    main()
