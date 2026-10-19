from app.db.database import connect_db, register_user
from app.services.security import hash_password

async def create_user(user):
    username: str = user.username.lower()
    email: str= user.email.lower()
    password: str= hash_password(user.password)
    conn = await connect_db()
    try:     
        user = await register_user(conn, username, email, password)
        if user == "already_exist":
            return "already_exist"
        else:
            return "created"
    finally:
        if conn is not None:
            await conn.close()