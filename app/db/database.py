import os
import sqlite3 as syncdb
from sqlite3 import IntegrityError, Connection as conn
import uuid
from app.db.queries import UserQueries

 
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "userDB.db")
DB_EXIST = os.path.exists(DB_PATH)


def create_db() -> None:
    connect = syncdb.connect(DB_PATH, timeout=30.0)
    connect.execute(UserQueries.JOURNAL_MODE)
    connect.execute(UserQueries.CREATE_TABLE)
    connect.commit()

if not DB_EXIST:
    create_db()

def connect_db() -> conn:
    conn = syncdb.connect(DB_PATH)
    return conn

def register_user(conn: conn, username: str, email: str,psswd: str) -> str:
    try:  
        with conn:
            cur = conn.cursor()
            user_id = str(uuid.uuid4())
            cur.execute(UserQueries.REGISTER_USER, (user_id , username, email, psswd))
            conn.commit()
            return "created"
    except IntegrityError:
        return "already_exist"

def get_id(conn: conn, email: str):
    with conn:
        cur = conn.cursor()
        cur.execute(UserQueries.GET_ID, (email,))

        row = cur.fetchone()
        if row == None: 
            return None
        return row[0]

def verify_id(conn:conn, id):
    with conn:
        cur = conn.cursor()
        cur.execute(UserQueries.VERIFY_ID, (id,))

        row = cur.fetchone()
        if row is not None:
            return row[0]
        return None

def get_hash(conn: conn, email: str):
    with conn:
        cur = conn.cursor()
        cur.execute(UserQueries.GET_HASH, (email,))
        
        row = cur.fetchone()
        if row is not None:
            return row[0]
        return None

