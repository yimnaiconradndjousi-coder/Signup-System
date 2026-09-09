from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
import string
from schema import SignupData

from rich import print

app = Flask(__name__)
CORS(app, origins="http://localhost:8080")

def validate_user_data(user):
    username = user['username']
    email = user['email']
    password = user['password']

@app.post('/signup')
def get_user_data():
    try:
        user = SignupData.model_validate(request.json)
    except ValidationError as error:
        return jsonify({
            "message": "Invalid data",
            "errors": error.errors()
        }), 400


    username = user.username
    email = user.email
    psswd = user.password
    print(username, email, psswd)

    if any(char in string.punctuation for char in username):
        return jsonify({
            "message": "Invalid username",
        }), 400

    return jsonify({"message":"User created successfully"}), 201

username = 1209
print(isinstance(username, str))

if __name__ == "__main__":
    app.run('localhost', 8080, debug=True)