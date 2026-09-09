from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from schema import SignupData
import string
from rich import print
# import asyncio
from db.database import initiate_db, check_user, register_user


app = Flask(__name__)
CORS(app, origins="http://localhost:8080")

async def Signup(user):
    username = user.username
    email = user.email
    password = user.password

    print(username, email, password)
    # conn = await initiate_db()
    # await register_user(conn, username, email, password)

@app.post('/signup')
async def fetch_user_data():
    user = await request.json
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