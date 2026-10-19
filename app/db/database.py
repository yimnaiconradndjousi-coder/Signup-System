import os
import sqlite3 as syncdb
import aiosqlite as asyncdb
import uuid
from aiosqlite import Connection as conn
 
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "userDB.db")
DB_EXIST = os.path.exists(DB_PATH)


def create_db() -> None:
    connect = syncdb.connect(DB_PATH)
    connect.execute("PRAGMA journal_mode=WAL;")
    connect.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY NOT NULL,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)
    connect.commit()

if not DB_EXIST:
    create_db()

async def connect_db() -> conn:
    conn = await asyncdb.connect(DB_PATH)
    return conn

async def register_user(conn: conn, username: str, email: str,psswd: str) -> str:
    cur = await conn.cursor()
    id = str(uuid.uuid4())
    try:  
        await cur.execute("""
            INSERT INTO users(
            id, 
            username, 
            email, 
            password_hash) 
            VALUES (?, ?, ?, ?);
        """, (id , username, email, psswd))
        await conn.commit()
        return "created"
    except LookupError:
        return "already_exist"


async def check_user(conn: conn, username: str, email: str):
    cur = await conn.cursor()
    try:
        await cur.execute(
            """
            SELECT username, email
            FROM users
            WHERE username = ? OR email = ?;
            """, (username, email))
    except LookupError:
        print("failed to check user")

    row = await cur.fetchone()
    if row is not None:
        return row[0]
    return None

async def get_id(conn: conn, email: str):
    cur = await conn.cursor()
    try: 
        await cur.execute("""
            SELECT id
            FROM users
            WHERE email = ?;
            """, (email,))
    except LookupError:
        print("user not found")

    row = await cur.fetchone()
    if row is not None:
        return row[0]
    return None

async def verify_id(conn:conn, id):
    cur = await conn.cursor()
    await cur.execute("""
        SELECT id
        FROM users
        WHERE id = ?;
        """, (id,))

    row = await cur.fetchone()
    if row is not None:
        return row[0]
    return None

async def get_hash(conn: conn, email: str):
    cur = await conn.cursor()
    try:
        await cur.execute("""
            SELECT password_hash
            FROM users
            WHERE email = ?;
            """, (email,))
    except LookupError:
        print("user not found")

    row = await cur.fetchone()
    if row is not None:
        return row[0]
    return None

