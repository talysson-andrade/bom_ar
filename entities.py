from typing import List
import requests

class ArCondicionado:
    def __init__(self, nome:str, marca:str, capacidade:int, index:int | None = None):
        self.nome:str = nome
        self.marca:str = marca
        self.index = index
        self.capacidade_total:int = capacidade
        dados = self.__get_valores()
        self.estaLigado:bool = dados["estado"]
        self.capacidade_atual = dados["capacidadeAtual"]
        self.temperatura_sensor = dados["temperaturaSensor"]

    def regularPotencia(self, fatorPotencia:float) -> None:
        capacidade_atual = int(float(self.capacidade_total) * fatorPotencia)
        print(f"A capacidade atual do Ar-condicionado {self.nome} foi ajustada para {capacidade_atual}")

    def getTemperaturaSensor(self) -> float:
        return self.temperatura_sensor
    
    def ligar(self) -> None:
        if self.estaLigado == True:
            print(f"O Ar-condicionado {self.nome} já está ligado")
            return
        self.estaLigado = True
        print(f"Ar-condicionado {self.nome} foi Ligado")
        return

    def desligar(self) -> None:
        if self.estaLigado == False:
            print(f"Ar-condicionado {self.nome} já está desligado")
            return
        self.estaLigado = False
        print(f"Ar-condicionado {self.nome} foi desligado")
        return

    def getCapacidadeAtual(self) -> int:
        return self.capacidade_atual

    def checarStatus(self) -> bool:
        return self.estaLigado
    
    def modoBaixoConsumo(self) -> None:
        print(f"Ativando modo de baixo consumo ativado no ar-condicionado {self.nome}")
        self.regularPotencia(0.1)
        return
    
    def __get_valores(self):
        try:
            resposta = requests.get(f"http://localhost:5000/ar/{self.index}")
            dados = resposta.json()
            return dados
        except Exception as e:
            return {"temperaturaSensor": 25.0, "capacidadeAtual": 0, "estado": False}

class Ambiente:
    def __init__(self, nome:str, temperaturaDesejada:float, cidade:str, ares_condicionados:List[ArCondicionado] | None = None, id:int | None = None):
        self.nome:str = nome
        self.temperaturaDesejada:float = temperaturaDesejada
        self.cidade:str = cidade
        self.ares_condicionados:List[ArCondicionado] = ares_condicionados or []
        self.id = id

    def adicionarArCondicionado(self, ar_condicionado:ArCondicionado) -> None:
        self.ares_condicionados.append(ar_condicionado)
        print(f"Ar-condicionado {ar_condicionado.nome} foi adicionado a {self.nome}")
        return

    def removerArCondicionado(self, ar_condicionado:ArCondicionado) -> None:
        self.ares_condicionados.remove(ar_condicionado)
        print(f"Ar-condicionado {ar_condicionado.nome} foi removido de {self.nome}")
        return

    def getTemperaturaSala(self) -> float:
        temp_total:float = 0.0
        if not self.ares_condicionados:
            return 0.0
        for ar in self.ares_condicionados:
            temp_total += ar.getTemperaturaSensor()
        temp_sala:float = temp_total / float(len(self.ares_condicionados))
        return temp_sala

    def getCargaTermica(self):
        carga_termica = 0
        if not self.ares_condicionados:
            return carga_termica
        for ar in self.ares_condicionados:
            carga_termica += ar.capacidade_total
        return carga_termica
