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
    if valores_gerados is None:
        return jsonify(None)
    for ar in valores_gerados:
        if ar["id"] == ar_id:
            ar_condicionado = ar
    return jsonify(ar_condicionado)

def gerar_valores():
    valores_gerados = []
    ares = db.get_todos_ares()
    if ares is None:
        return
    for ar in ares:
        temperatura_sensor = random.uniform(24.0, 35.0)
        estado = bool(random.randint(0,1))
        capacidade_atual = random.randint(1000, ar["capacidadeTotal"])
        valores_gerados.append({"id": ar["id"],"temperaturaSensor": temperatura_sensor, "estado": estado, "capacidadeAtual": capacidade_atual})
        print(valores_gerados[-1])
    return valores_gerados

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
