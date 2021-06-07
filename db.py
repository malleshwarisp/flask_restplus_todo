import sqlite3
from typing import Optional

con: Optional[sqlite3.Connection] = None


def get_db():
    global con
    if not con:
        con = sqlite3.connect("todo_app.db")
    return con


def close_db():
    global con
    if con:
        con.close()
    con = None
