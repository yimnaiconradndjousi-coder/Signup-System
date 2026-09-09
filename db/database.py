import aiosqlite as db
import uuid
from datetime import datetime

async def initiate_db():
    conn = await db.connect('./userDB')
    await conn.execute("PRAGMA journal_mode=WAL;")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        date DATE NOT NULL,
        UNIQUE(username, email)
        )
        """)
    return conn

async def check_user(conn, username: str, email: str) -> list:
    cur = conn.cursor()
    query = None
    try:
        query = await cur.execute(
            """
            SELECT username, email
            FROM users
            WHERE username = ? AND email = ?;
            """, (username, email))
    except LookupError:
        print("failed to check user")

    query_result =  query.fetchall()
    return query_result

async def register_user(conn, username: str, email: str, psswd: str) -> None:
    cur = await conn.cursor()
    id = uuid.uuid1()
    now = datetime.now()
    date_time = now.strftime("%Y/%m/%d %H:%M:%S")

    try:  
        query = await cur.execute("""
        INSERT INTO users(id, username, email, password, date) VALUES (?, ?, ?, ?, ?);
        """, (id , username, email, psswd, date_time))
        print("User Register successfully")
    except LookupError:
        print("Failed to register user")

            

