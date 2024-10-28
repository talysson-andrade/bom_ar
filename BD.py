import mysql.connector
from tkinter import *
from tkinter import messagebox

mydb = None

def configurar_banco():
    global mydb
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )

        cursor = mydb.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS teste")
        mydb.database = 'teste'

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ambiente (
                id_Ambiente UNIQUE INT AUTO_INCREMENT PRIMARY ,
                nome VARCHAR(100),
                temperatura_desejada FLOAT,
                localização VARCHAR(100)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ar_condicionado (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255),
                marca VARCHAR(100),
                Capacidade_BTUs INT,
                ambiente_id INT,
                FOREIGN KEY (ambiente_id) REFERENCES Ambiente(id_Ambiente) ON DELETE CASCADE
            )
        """)

        mydb.commit()
        cursor.close()
        messagebox.showinfo()

    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao configurar banco de dados: {err}")

def consultar_ambientes():
    global mydb
    cursor = None
    if mydb is None:
        messagebox.showwarning("Aviso", "Conexão com o banco de dados não configurada.")
        return

    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM Ambiente")
        ambientes = cursor.fetchall()
        
        print("Ambientes:")
        for ambiente in ambientes:
            print(ambiente)
            
            cursor.execute("SELECT * FROM Ar_condicionado WHERE ambiente_id = %s", (ambiente[0],))
            ar_condicionados = cursor.fetchall()
            print("  Ar Condicionado:")
            for ar in ar_condicionados:
                print(f"    {ar}")

    except Exception as erro:
        print("Erro:", erro)

    finally:
        if cursor:
            cursor.close()

def adicionar_ambiente(nome, temperatura_desejada, localizacao):
    global mydb
    cursor = None

    if mydb is None:
        configurar_banco()

    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO Ambiente (nome, temperatura_desejada, localização) VALUES (%s, %s, %s)",
                       (nome, temperatura_desejada, localizacao))
        mydb.commit()
        messagebox.showinfo("Sucesso", "Ambiente adicionado com sucesso!")

    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao adicionar ambiente: {erro}")

    finally:
        if cursor:
            cursor.close()

def deletar_ambiente(id_ambiente):
    global mydb
    cursor = None
    if mydb is None:
        messagebox.showwarning("Aviso", "Conexão com o banco de dados não configurada.")
        return

    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Ambiente WHERE id_Ambiente = %s", (id_ambiente,))
        mydb.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Sucesso", "Ambiente deletado com sucesso!")
        else:
            messagebox.showwarning("Atenção", "ID do ambiente não encontrado.")

    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao deletar ambiente: {erro}")

    finally:
        if cursor:
            cursor.close()

def consultar_ar_condicionado():
    global mydb
    cursor = None
    if mydb is None:
        messagebox.showwarning("Aviso", "Conexão com o banco de dados não configurada.")
        return

    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM Ar_condicionado")
        registros = cursor.fetchall()

        print("Ar Condicionado:")
        for registro in registros:
            print(registro)

    except Exception as erro:
        print("Erro:", erro)

    finally:
        if cursor:
            cursor.close()

def adicionar_ar_condicionado(nome, marca, capacidade_btus, ambiente_id):
    global mydb
    cursor = None
    if mydb is None:
        messagebox.showwarning("Aviso", "Conexão com o banco de dados não configurada.")
        return

    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO Ar_condicionado (nome, marca, Capacidade_BTUs, ambiente_id) VALUES (%s, %s, %s, %s)",
                       (nome, marca, capacidade_btus, ambiente_id))
        mydb.commit()
        messagebox.showinfo("Sucesso", "Ar condicionado adicionado com sucesso!")

    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao adicionar ar condicionado: {erro}")

    finally:
        if cursor:
            cursor.close()

def deletar_ar_condicionado(id_ar):
    global mydb
    cursor = None
    if mydb is None:
        messagebox.showwarning("Aviso", "Conexão com o banco de dados não configurada.")
        return

    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM Ar_condicionado WHERE id = %s", (id_ar,))
        mydb.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Sucesso", "Ar condicionado deletado com sucesso!")
        else:
            messagebox.showwarning("Atenção", "ID do ar condicionado não encontrado.")

    except Exception as erro:
        messagebox.showerror("Erro", f"Erro ao deletar ar condicionado: {erro}")

    finally:
        if cursor:
            cursor.close()

def main():
    global mydb
    root = Tk()
    root.title("Interface do Banco de Dados")

   
    Label(root, text="Nome Ambiente:").pack()
    nome_entry = Entry(root)
    nome_entry.pack()

    Label(root, text="Temperatura Desejada:").pack()
    temp_entry = Entry(root)
    temp_entry.pack()

    Label(root, text="Localização:").pack()
    local_entry = Entry(root)
    local_entry.pack()

    botao_adicionar = Button(root, text="Adicionar Ambiente", command=lambda: adicionar_ambiente(nome_entry.get(), temp_entry.get(), local_entry.get()))
    botao_adicionar.pack(pady=10)
   
    Label(root, text="ID do Ambiente para Deletar:").pack()
    id_entry = Entry(root)
    id_entry.pack()

    botao_deletar = Button(root, text="Deletar Ambiente", command=lambda: deletar_ambiente(id_entry.get()))
    botao_deletar.pack(pady=10)
    
    botao_consultar_ambientes = Button(root, text="Consultar Ambientes", command=consultar_ambientes)
    botao_consultar_ambientes.pack(pady=10)

    
    Label(root, text="Nome Ar Condicionado:").pack()
    ar_nome_entry = Entry(root)
    ar_nome_entry.pack()

    Label(root, text="Marca:").pack()
    ar_marca_entry = Entry(root)
    ar_marca_entry.pack()

    Label(root, text="Capacidade BTUs:").pack()
    ar_btus_entry = Entry(root)
    ar_btus_entry.pack()

    Label(root, text="ID do Ambiente:").pack()
    ar_ambiente_id_entry = Entry(root)
    ar_ambiente_id_entry.pack()

    botao_adicionar_ar = Button(root, text="Adicionar Ar Condicionado", command=lambda: adicionar_ar_condicionado(ar_nome_entry.get(), ar_marca_entry.get(), ar_btus_entry.get(), ar_ambiente_id_entry.get()))
    botao_adicionar_ar.pack(pady=10)

    
    Label(root, text="ID do Ar Condicionado para Deletar:").pack()
    ar_id_entry = Entry(root)
    ar_id_entry.pack()

    botao_deletar_ar = Button(root, text="Deletar Ar Condicionado", command=lambda: deletar_ar_condicionado(int(ar_id_entry.get())))
    botao_deletar_ar.pack(pady=10)

    
    botao_consultar_ar = Button(root, text="Consultar Ar Condicionado", command=consultar_ar_condicionado)
    botao_consultar_ar.pack(pady=10)

    root.mainloop()
   
    if mydb:
        mydb.close()

if __name__ == "__main__":
    main()
