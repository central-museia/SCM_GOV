from database.connection import conectar


def criar_banco():
    conn = conectar()

    cursor = conn.cursor()

    # criação das tabelas

    conn.commit()
    conn.close()
