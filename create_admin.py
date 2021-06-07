from sqlite3 import IntegrityError

from db import close_db, get_db
from users.password_hash import hash_password


def create_admin(username: str, password: str):
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, permission) VALUES (?,?,7)",
            (username, hash_password(password)),
        )
        db.commit()
    except IntegrityError:
        print("Username already exists")
    close_db()


if __name__ == "__main__":
    import sys

    create_admin(sys.argv[1], sys.argv[2])
