from flask import Flask, jsonify
from typing import List
from entities import ArCondicionado
import db
import random

app = Flask("bom_ar")
    
@app.route('/ar/<int:ar_id>', methods=["GET"])
def get_info_ar(ar_id):
    ar_condicionado = None
    valores_gerados = gerar_valores()
    for ar in valores_gerados:
        if ar["id"] == ar_id:
            ar_condicionado = ar
    return jsonify(ar_condicionado)

def get_ares(): 
    ambientes = db.get_ambientes()
    print(len(ambientes))
    ares:List[ArCondicionado] = []
    for ambiente in ambientes:
        for ar in ambiente.ares_condicionados:
            ares.append(ar)
    return ares

def gerar_valores():
    valores_gerados = []
    ares = get_ares()
    for ar in ares:
        temperatura_sensor = random.uniform(24.0, 35.0)
        estado = bool(random.randint(0,1))
        capacidade_atual = random.randint(1000, ar.capacidade_total)
        valores_gerados.append({"id": ar.index,"temperaturaSensor": temperatura_sensor, "estado": estado, "capacidadeAtual": capacidade_atual})
    return valores_gerados

if __name__ == "__main__":
    app.run(host="localhost", port="5000")