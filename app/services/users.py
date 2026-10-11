from app.db.database import initiate_db, check_user, register_user
from app.services.security import hash_password

async def create_user(user):
    username: str = user.username.lower()
    email: str= user.email.lower()
    password: str= hash_password(user.password)
    conn = None
    try:     
        conn = await initiate_db()
        user = await register_user(conn, username, email, password)

        if user == "already_exist":
            return "already_exist"
        else:
            return "created"

    except ValueError:
        return "user registry Failed"

    finally:
        if conn is not None:
            await conn.close()