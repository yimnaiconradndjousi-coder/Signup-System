from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.schema import SignupData
import string
from app.services.users import create_user

register = Blueprint("register0", __name__, url_prefix="/api")

@register.post("/register")
async def signup():
    user = request.get_json(silent=True)
    try:
        user = SignupData.model_validate(user)
    except ValidationError:
        return jsonify({
            "message": "Invalid input",
            "errors": {
                "username":"Name must be have a minimum of 3 letters, and munt not contain special char.",
                "email":"enter a valid Email",
                "password": "Password must be at least 8 characters"
            }
        }), 400
    
    username = user.username
    if any(char in string.punctuation for char in username):
        return jsonify({
            "message": "Invalid input",
            "errors": {
                "username":"Name must be have a minimum of 3 letters, and must not contain special char.",
                "email":"enter a valid Email",
                "password": "Password must be at least 8 characters"
            }
        }), 400
    
    result = await create_user(user)

    if result == "already_exist":
        return jsonify({"message": "An account with this username or email already exist"}), 409
    elif result == "created":
        return jsonify({"message":"User created successfully"}), 201
    else:
        return jsonify({"message": "Something went wrong"}), 500
