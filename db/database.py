import aiosqlite as db
import uuid
from datetime import datetime

async def initiate_db():
    conn = await db.connect('./db/userDB.db')
    await conn.execute("PRAGMA journal_mode=WAL;")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY NOT NULL,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash  NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    return conn

async def check_user(conn: db.Connection, username: str, email: str) -> list:
    cur = await conn.cursor()
    query = None
    try:
        query = await cur.execute(
            """
            SELECT username, email
            FROM users
            WHERE username = ? OR email = ?;
            """, (username, email))
    except LookupError:
        print("failed to check user")

    query_result = await query.fetchone()
    return query_result

async def register_user(conn: db.Connection, username: str, email: str, psswd: str) -> None:
    cur = await conn.cursor()
    id = str(uuid.uuid1())

    try:  
        query = await cur.execute("""
        INSERT INTO users(id, username, email, password_hash) VALUES (?, ?, ?, ?);
        """, (id , username, email, psswd))
        await conn.commit()
        print("User Register successfully")
    except LookupError:
        print("Failed to register user")

            

