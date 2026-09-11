import aiosqlite as db
import uuid
from aiosqlite import Connection as conn

async def initiate_db() -> conn:
    conn = await db.connect('./db/userDB.db')
    await conn.execute("PRAGMA journal_mode=WAL;")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY NOT NULL,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    return conn

async def register_user(conn: conn, username: str, email: str,psswd: str) -> None:
    cur = await conn.cursor()
    id = str(uuid.uuid1())
    try:  
        await cur.execute("""
            INSERT INTO users(id, username, email, password_hash) VALUES (?, ?, ?, ?);
        """, (id , username, email, psswd))
        await conn.commit()
        print("User Register successfully")
    except LookupError:
        print("Failed to register user")


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

    query_result = await cur.fetchone()
    return query_result

async def get_id(conn: conn, username, email):
    cur = await conn.cursor()
    try: 
        await cur.execute("""
            SELECT id
            FROM users
            WHERE username = ? AND email = ?;
            """, (username, email))
    except LookupError:
        print("user not found")
    return await cur.fetchone()

async def get_hash(conn: conn, username, email):
    cur = await conn.cursor()
    try:
        await cur.execute("""
            SELECT password_hash
            FROM users
            WHERE username = ? AND email = ?;
            """, (username, email))
    except LookupError:
        print("user not found")
    return await cur.fetchone()

