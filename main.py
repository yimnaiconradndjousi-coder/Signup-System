from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from schema import SignupData
from db.database import initiate_db, check_user, register_user
import bcrypt
from rich import print
import string

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080", "http://localhost:5500"])

def password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_psswd = bcrypt.hashpw(password_bytes, salt)
    hashed_psswd_string = hashed_psswd.decode("utf-8")
    return hashed_psswd_string

async def Signup(user):
    username: str = user.username.lower()
    email: str= user.email
    password: str= password_hash(user.password)
    conn = None
    try:     
        conn = await initiate_db()
        users = await check_user(conn, username, email)
        print(users)
        if users is None:
            await register_user(conn, username, email, password)
        else:
            print('User already exist.')

    except ValueError:
        print("Sign up failed")

    finally:
        if conn is not None:
            await conn.close()


@app.post('/signup')
async def fetch_user_data():
    user = request.get_json(silent=True)
    try:
        user = SignupData.model_validate(user)
    except ValidationError as error:
        return jsonify({
            "message": "Invalid data",
            "errors": error.errors()
        }), 400

    username = user.username
    if any(char in string.punctuation for char in username):
        return jsonify({
            "message": "Invalid username",
        }), 400

    await Signup(user)

    return jsonify({"message":"User created successfully"}), 201

if __name__ == "__main__":
    app.run('localhost', 8080, debug=True)