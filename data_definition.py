from db import get_db, close_db

db_con = get_db()


def create_tasks_table():
    cur = db_con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT,
        due_by DATE,
        status INTEGER
    )"""
    )
    db_con.commit()


def create_users_table():
    cur = db_con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username VARCHAR(30),
            password_hash BLOB,
            permission INTEGER
        )"""
    )
    cur.execute("CREATE UNIQUE INDEX idx_username ON users(username)")
    db_con.commit()


def create_all_tables():
    create_users_table()
    create_tasks_table()
    close_db()


if __name__ == "__main__":
    create_all_tables()
