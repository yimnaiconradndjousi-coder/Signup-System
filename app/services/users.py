from app.db.database import connect_db, register_user
from app.services.security import hash_password

def create_user(user):
    username: str = user.username.lower()
    email: str= user.email.lower()
    password: str= hash_password(user.password)
    conn = connect_db()
    try:     
        user = register_user(conn, username, email, password)
        if user == "already_exist":
            return "already_exist"
        else:
            return "created"
    finally:
        conn.close()