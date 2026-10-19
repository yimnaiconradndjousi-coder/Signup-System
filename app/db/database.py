import os
import sqlite3 as syncdb
import aiosqlite as asyncdb
import uuid
from aiosqlite import IntegrityError , Connection as conn
from app.db.queries import UserQueries

 
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "userDB.db")
DB_EXIST = os.path.exists(DB_PATH)


def create_db() -> None:
    connect = syncdb.connect(DB_PATH)
    connect.execute(UserQueries.JOURNAL_MODE)
    connect.execute(UserQueries.CREATE_TABLE)
    connect.commit()

if not DB_EXIST:
    create_db()

async def connect_db() -> conn:
    conn = await asyncdb.connect(DB_PATH)
    return conn

async def register_user(conn: conn, username: str, email: str,psswd: str) -> str:
    async with conn.cursor() as cur:
        user_id = str(uuid.uuid4())
        try:  
            await cur.execute(UserQueries.REGISTER_USER, (user_id , username, email, psswd))
            await conn.commit()
            return "created"
        except IntegrityError:
            return "already_exist"

async def get_id(conn: conn, email: str):
    async with conn.cursor() as cur:
        await cur.execute(UserQueries.GET_ID, (email,))
        row = await cur.fetchone()
        if row == None: 
            return None
        return row[0]

async def verify_id(conn:conn, id):
    async with conn.cursor() as cur:
        await cur.execute(UserQueries.VERIFY_ID, (id,))
        row = await cur.fetchone()
        if row is not None:
            return row[0]
        return None

async def get_hash(conn: conn, email: str):
    async with conn.cursor() as cur:
        await cur.execute(UserQueries.GET_HASH, (email,))
        
        row = await cur.fetchone()
        if row is not None:
            return row[0]
        return None

