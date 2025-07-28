import sqlite3

# Conecta no banco (ele cria o arquivo se não existir)
conn = sqlite3.connect('usuarios.db')

# Cria a tabela
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

# Salva e fecha
conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
