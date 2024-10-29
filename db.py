from contextlib import closing
from typing import List
from entities import ArCondicionado, Ambiente
import mysql.connector
from os import getenv

USER = getenv("AR_DB_USER")
HOST = getenv("AR_DB_HOST")
DATABASE = getenv("AR_DB_DATABASE")
PASSWORD = getenv("AR_DB_PASSWORD")

def run_query(query:str, values:tuple | None = None):
    with closing(mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)) as connection:
        with closing(connection.cursor()) as cursor:
            if values: cursor.execute(query, values)
            else: cursor.execute(query)
            warning = cursor.fetchwarnings()
            if warning is not None: raise Exception(f"Retornou aviso: {warning}")
            rows = cursor.fetchall()
            connection.commit()
        return rows

def insert_ambiente(ambiente:Ambiente):
    query = """
    INSERT INTO Ambiente (nome, temperatura_desejada, cidade)
    VALUES (%s, %s, %s)
    """
    values = (ambiente.nome, ambiente.temperaturaDesejada, ambiente.cidade,)
    
    try:
        run_query(query, values)
        print(f"O Ambiente {ambiente.nome} foi adicionado ao Banco de Dados")

    except Exception as e:
        print(f"Houve um erro ao adicionar o ambiente {ambiente.nome} ao Banco de Dados: {e}")

def insert_ar(ar:ArCondicionado, ambiente_id:int):
    query = """
        INSERT INTO Ar_condicionado (nome, marca, capacidade, ambiente_id)
        VALUES (%s, %s, %s, %s)
        """
    values = (ar.nome, ar.marca, ar.capacidade_total, ambiente_id)

    try:
        run_query(query,values)
        print(f"O Ar_condicionado {ar.nome} foi adicionado ao Banco de Dados")
    except Exception as e:
        print(f"Houve um erro ao adicionar o Ar_condicionado {ar.nome} ao Banco de Dados: {e}")

def get_ambientes():
    ambientes:List[Ambiente] = []
    query = """
        SELECT * FROM Ambiente
        """
    try:
        rows = run_query(query)
        for row in rows:
            ares = get_ares(row[0])
            if not ares:
                ares = None
            ambiente = Ambiente(row[1],row[2], row[3], ares_condicionados=ares, id=row[0])
            ambientes.append(ambiente)
        return ambientes
    except Exception as e:
        print(f"Houve um erro ao buscar Ambientes no Banco de Dados: {e}")
        return

def alterar_ambiente(ambiente:Ambiente):
    query = """
    UPDATE Ambiente 
    SET nome = %s, temperatura_desejada = %s
    WHERE id = %s 
    """
    values = (ambiente.nome, ambiente.temperaturaDesejada, ambiente.id,)
    try:
        run_query(query, values)
        print("Ambiente atualizado")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o Ambiente: {e}")
        return

def get_ares(ambiente_id):
    ares:List[ArCondicionado] = []
    query = """
        SELECT * FROM Ar_condicionado WHERE ambiente_id = %s
        """
    values = (ambiente_id,)
    try:
        rows = run_query(query, values)
        for row in rows:
            ar = ArCondicionado(nome=row[1], marca=row[2], capacidade=row[3])
            ares.append(ar)
        return ares
    except Exception as e:
        print(f"Houve um erro ao buscar Ares_condicionados no Banco de Dados: {e}")
        return


