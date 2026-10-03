from flask import Blueprint, request, jsonify, session
from app.db.database import initiate_db, get_hash, get_id, verify_id
from pydantic import ValidationError
from app.schema import LoginData
from app.services.security import verify_password

auth = Blueprint("auth0", __name__, url_prefix="/api/auth")

@auth.post("/login")
async def login():
    user = request.get_json(silent=True)
    try:
        user = LoginData.model_validate(user)
    except ValidationError as error:
        return jsonify({
            "message": "Invalid input",
            "errors": error.errors()
        }), 400

    conn = await initiate_db()
    email = user.email.lower()
    password = user.password
    user_id = await get_id(conn, email)
    try:
        stored_psswd_hash = await get_hash(conn, email)
        if stored_psswd_hash is None:
            return jsonify({"message": "No account exists for this username or email"}), 400

        is_hash_valid = verify_password(password, stored_psswd_hash) 

        if is_hash_valid:
            session.clear()
            session['session_id'] = user_id
            session.permanent = True
            return jsonify({"message": "Login successful"}), 202
        else:
            return jsonify({"message": "Invalid Email or Password"}), 400
        
    except ValueError:
        return jsonify({'message': "Something went wrong, Invalid Email or Password"}), 400
    
    finally:
        await conn.close()


@auth.post("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200


@auth.post("/me")
async def current_user():
    session_id = session.get('session_id')
    if session_id is None:
        return jsonify({"message": "Authentication required"}), 401

    conn = await initiate_db()
    try:
        id = verify_id(conn, session_id)
    finally:
        await conn.close()

    if id is None:
        session.clear()
        return jsonify({"id": session_id})
    
    return jsonify({"message": "Authentication required"}),  401
