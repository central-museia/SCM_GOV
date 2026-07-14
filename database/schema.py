"""
Schema do banco

Autor: SCM Engenharia
"""

from database.connection import conectar


def criar_banco():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        chave TEXT,

        valor TEXT

    )
    """)

    conn.commit()

    conn.close()
