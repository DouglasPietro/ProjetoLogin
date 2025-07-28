import sqlite3

conn = sqlite3.connect('usuarios.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    telefone TEXT,
    senha TEXT NOT NULL,
    servico TEXT
);
''')
conn.commit()
conn.close()

print("Banco de dados recriado com sucesso!")
