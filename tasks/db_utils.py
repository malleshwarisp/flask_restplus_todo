from datetime import date
from db import get_db
from sqlite3 import Connection
from enum import Enum


class Status(Enum):
    NOTSTARTED = 0
    INPROGRESS = 1
    FINISHED = 2


def create_task(db: Connection, task: str, due_by: date, status=Status.NOTSTARTED):
    cur = db.cursor()
    cur.execute(
        "INSERT INTO tasks (task, due_by, status) VALUES (?,?,?)",
        (task, due_by, status.value),
    )
    db.commit()
    result = cur.execute(
        "SELECT (id, task, due_by, status) FROM tasks WHERE id=?", (cur.lastrowid,)
    )
    return result.fetchone()


def get_all_tasks(db: Connection):
    cur = db.cursor()
    results = cur.execute("SELECT (id, task, due_by, status) FROM tasks")
    return results.fetchall()


def get_task(db: Connection, id: int):
    cur = db.cursor()
    result = cur.execute(
        "SELECT (id, task, due_by, status) FROM tasks WHERE id=?", (id,)
    )
    return result.fetchone()


def update_task(db: Connection, id: int, task: str, due_by: date, status: Status):
    if not get_task(db, id):
        return False
    cur = db.cursor()
    cur.execute(
        "UPDATE tasks SET task=?, due_by=?, status=? WHERE id=?",
        (task, due_by, status.value, id),
    )
    db.commit()
    result = cur.execute(
        "SELECT (id, task, due_by, status) FROM tasks WHERE id=?", (cur.lastrowid,)
    )
    return result.fetchone()


def update_status(db: Connection, id: int, status: Status):
    if not get_task(db, id):
        return False
    cur = db.cursor()
    cur.execute("UPDATE tasks SET  status=? WHERE id=?", (status.value, id))
    db.commit()


def delete_task(db: Connection, id: int):
    if not get_task(db, id):
        return False
    cur = db.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    db.commit()


def tasks_by_due_date(db: Connection, due_by: date):
    cur = db.cursor()
    result = cur.execute(
        "SELECT (id, task, due_by, status) FROM tasks WHERE due_by=?", (due_by,)
    )
    return result.fetchall()


def tasks_overdue(db: Connection):
    cur = db.cursor()
    result = cur.execute(
        "SELECT (id, task, due_by, status) FROM tasks WHERE due_by=?", (date.today(),)
    )
    return result.fetchall()


def tasks_finished(db: Connection):
    cur = db.cursor()
    result = cur.execute(
        "SELECT (id, task, due_by, status) FROM tasks WHERE status=?",
        (Status.FINISHED.value,),
    )
    return result.fetchall()
