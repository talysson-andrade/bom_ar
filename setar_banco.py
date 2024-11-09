#Este é somente um script para setar o banco de dados para rodar o código
#Dentro do arquivo bom_ar_db.sql contem as tabelas e alguns dados mas também precisamos setar um novo schema
#Para usar a aplicação é necessário ter um banco MySQL disponível

#Este script irá criar um novo schema com o nome adicionado a variável de ambiente "AR_DB_DATABASE"
#Lembre-se adicionar as variaveis de ambiente para rodar esse script

#AR_DB_DATABASE  -  Nome do banco/schema
#AR_DB_USER   -  Usuário do banco de dados 
#AR_DB_PASSWORD   -  Senha de acesso do usuário
#AR_DB_HOST   -   host do banco de dados, caso o banco esteja rodando localmente pode ser setado como 'localhost'. caso esteja rodando remotamente deve conter o domínio/ip


from os import getenv
import mysql.connector

USER = getenv("AR_DB_USER")
HOST = getenv("AR_DB_HOST")
DATABASE = getenv("AR_DB_DATABASE")
PASSWORD = getenv("AR_DB_PASSWORD")

mydb = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
)

cursor = mydb.cursor()
query = f"CREATE DATABASE IF NOT EXISTS {DATABASE} DEFAULT CHARACTER SET utf8 COLLATE utf8_bin"
cursor.execute(query)

mydb.database = DATABASE
mydb.set_charset_collation("utf8")

script = ""

with open("bom_ar_db.sql", "r") as file:
    script = file.read()
    file.close()

cursor.execute(script)
cursor.close()
mydb.close()