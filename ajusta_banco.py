import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Adiciona a coluna telefone caso ainda não exista
try:
    cursor.execute('ALTER TABLE usuarios ADD COLUMN telefone TEXT')
    print("Coluna telefone adicionada!")
except sqlite3.OperationalError:
    print("A coluna telefone já existe.")

conn.commit()
conn.close()
