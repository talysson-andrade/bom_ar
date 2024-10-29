from typing import List

class ArCondicionado:
    def __init__(self, nome:str, marca:str, capacidade:int):
        self.nome:str = nome
        self.marca:str = marca
        self.capacidade_total:int = capacidade
        self.estaLigado:bool = self.checarStatus()
        self.capacidade_atual:int = self.getCapacidadeAtual()

    def regularPotencia(self, fatorPotencia:float) -> None:
        self.capacidade_atual = int(float(self.capacidade_total) * fatorPotencia)
        print(f"A capacidade atual do Ar-condicionado {self.nome} foi ajustada para {self.capacidade_atual}")

    def getTemperaturaSensor(self) -> float:
        return 25.0
    
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
        return 12000

    def checarStatus(self) -> bool:
        return True

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

