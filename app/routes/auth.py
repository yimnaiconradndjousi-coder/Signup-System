from flask import Blueprint, request, jsonify, session
from app.db.database import connect_db, get_hash, verify_id
from pydantic import ValidationError
from app.schema import LoginData
from app.services.security import verify_password
from secrets import token_urlsafe

auth = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth.post("/login")
def login():
    user = request.get_json(silent=True)
    try:
        user = LoginData.model_validate(user)
    except ValidationError:
        return jsonify({
            "message": "Invalid Email or Password",
        }), 400

    conn = connect_db()
    email = user.email.lower()
    password = user.password

    stored_psswd_hash = get_hash(conn, email)
    if stored_psswd_hash is None:
        return jsonify({"message": "Invalid Email or Password"}), 400
    
    try:
        is_hash_valid = verify_password(password, stored_psswd_hash) 
        if is_hash_valid:
            session.clear()
            session['session_id'] = token_urlsafe(25)
            session.permanent = True
            return jsonify({"message": "Login successful"}), 202
        else:
            return jsonify({"message": "Invalid Email or Password"}), 400
        
    except ValueError:
        return jsonify({'message': "Invalid Email or Password"}), 400
    finally:
        conn.close()


@auth.post("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

@auth.post("/me")
def current_user():
    session_id = session.get('session_id')
    if session_id is None:
        return jsonify({"message": "Authentication required"}), 401

    conn = connect_db()
    try:
        id = verify_id(conn, session_id)
    finally:
        conn.close()

    if id:
        return jsonify({"id": session_id})
    
    return jsonify({"message": "Authentication required"}),  401
