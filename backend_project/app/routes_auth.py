from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from . import db
from .models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    username = (data.get("username") or "").strip()
    password = data.get("password")

    if not email or not password:
        return {"error": "email and password required"}, 400

    if db.session.query(User).filter(User.email == email).first():
        return {"error": "email already registered"}, 409

    u = User(email=email, username=username or None, password_hash="")
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return {"id": u.id, "email": u.email, "username": u.username}, 201

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return {"error": "email and password required"}, 400

    u = db.session.query(User).filter(User.email == email).first()
    if not u or not u.check_password(password):
        return {"error": "invalid_credentials"}, 401

    # identity stores the user id
    token = create_access_token(identity=str(u.id))
    return {"access_token": token, "user": {"id": u.id, "email": u.email}}, 200
