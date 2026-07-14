import sqlite3
from pathlib import Path

DATABASE = Path(__file__).parent / "scmgov.db"

def conectar():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn
