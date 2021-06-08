from sqlite3.dbapi2 import Connection, IntegrityError
from typing import List
from users.password_hash import hash_password

from db import get_db

from .permissions import Permission


def create_user(
    db: Connection, username: str, password: str, permissions: List[Permission]
):
    cur = db.cursor()
    password_hash = hash_password(password)
    permission_value = 0
    for permission in permissions:
        permission_value |= Permission[permission].value
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, permission) VALUES (?,?,?)",
            (username, password_hash, permission_value),
        )
        db.commit()
        result = cur.execute(
            "SELECT id, username, password_hash, permission FROM users WHERE id=?",
            (cur.lastrowid,),
        )
        return result.fetchone()
    except IntegrityError:
        return False


def get_users(db: Connection):
    cur = db.cursor()
    result = cur.execute("SELECT id, username, password_hash, permission FROM users")
    return result.fetchall()


def get_user_by_name(db: Connection, username: str):
    cur = db.cursor()
    result = cur.execute(
        "SELECT id, username, password_hash, permission FROM users WHERE username=?",
        (username,),
    )
    return result.fetchone()


def user_to_dict(user):
    if not user:
        return None
    permissions = []
    permission_value = user[3]
    for p in Permission:
        if permission_value & p.value == p.value:
            permissions.append(p.name)
    return {"id": user[0], "username": user[1], "permission": permissions}
