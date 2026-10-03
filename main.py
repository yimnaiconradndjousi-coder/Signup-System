# import os
# from dotenv import load_dotenv

# from flask import request, jsonify, session
# from app import app
# from app import routes
# from flask_cors import CORS
# from pydantic import ValidationError
# from app.schema import SignupData, LoginData
# from app.db.database import initiate_db, get_hash, get_id, verify_id
# from app.services.security import verify_password
# from services.users import create_user
# import string
# from rich import print

# load_dotenv()
# SECRET_KEY = os.getenv("SECRET_KEY")
# if not SECRET_KEY:
#     raise RuntimeError("SECRET_KEY is missing from .env")

# app.config.update(
#     SECRET_KEY= SECRET_KEY,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE="Lax",
#     SESSION_COOKIE_SECURE=True, 
#     PERMANENT_SESSION_LIFETIME=60 * 60 * 24 * 7,
# )

# CORS(app, origins=[
#     "http://localhost:8080",
#     "http://localhost:5500",
#     "http://127.0.0.1:5500"
#     ], supports_credentials = True
# )

# @app.post('/api/register')
# async def signup():
#     user = request.get_json(silent=True)
#     try:
#         user = SignupData.model_validate(user)
#     except ValidationError:
#         return jsonify({
#             "message": "Invalid input",
#             "errors": {
#                 "username":"Name must be have a minimum of 3 letters, and munt not contain special char.",
#                 "email":"enter a valid Email",
#                 "password": "Password must be at least 8 characters"
#             }
#         }), 400
    
#     username = user.username
#     if any(char in string.punctuation for char in username):
#         return jsonify({
#             "message": "Invalid input",
#             "errors": {
#                 "username":"Name must be have a minimum of 3 letters, and must not contain special char.",
#                 "email":"enter a valid Email",
#                 "password": "Password must be at least 8 characters"
#             }
#         }), 400
    
#     result = await create_user(user)

#     if result == "already_exist":
#         return jsonify({"message": "An account with this username or email already exist"}), 409
#     elif result == "created":
#         return jsonify({"message":"User created successfully"}), 201
#     else:
#         return jsonify({"message": "Something went wrong"}), 500


# @app.post('/api/auth/login')
# async def login():
#     user = request.get_json(silent=True)
#     try:
#         user = LoginData.model_validate(user)
#     except ValidationError as error:
#         return jsonify({
#             "message": "Invalid input",
#             "errors": error.errors()
#         }), 400

#     conn = await initiate_db()
#     email = user.email.lower()
#     user_id = await get_id(conn, email)
#     password = user.password
#     try:
#         stored_psswd_hash = await get_hash(conn, email)
#         if stored_psswd_hash is None:
#             return jsonify({"message": "No account exists for this username or email"}), 400

#         is_hash_valid = verify_password(password, stored_psswd_hash) 

#         if is_hash_valid:
#             session.clear()
#             session['session_id'] = user_id
#             print(user_id)
#             session.permanent = True
#             return jsonify({"message": "Login successful"}), 202
#         else:
#             return jsonify({"message": "Invalid Email or Password"}), 400
        
#     except ValueError:
#         return jsonify({'message': "Something went wrong, Invalid Email or Password"}), 400
    
#     finally:
#         await conn.close()

# @app.post("/api/auth/logout")
# def logout():
#     session.clear()
#     return jsonify({"message": "Logged out"}), 200

# @app.get('/api/auth/me')
# async def current_user():
#     session_id = session.get('session_id')
#     if session_id is None:
#         return jsonify({"message": "Authentication required"}), 401

#     conn = await initiate_db()
#     try:
#         id = verify_id(conn, session_id)
#     finally:
#         await conn.close()

#     if id is None:
#         session.clear()
#         return jsonify({"id": session_id})
    
#     return jsonify({"message": "Authentication required"}),  401


# if __name__ == "__main__":
#     app.run('localhost', 8080, debug=True) 