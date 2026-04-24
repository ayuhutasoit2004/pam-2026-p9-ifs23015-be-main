from flask import Blueprint, request, jsonify
import jwt
import datetime
from app.config import Config

auth_bp = Blueprint("auth", __name__)

def generate_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except Exception:
        return None


@auth_bp.route("/", methods=["GET"])
def index():
    return "TreePedia API - Aktif! 🌳"


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username dan password wajib diisi"}), 400

    if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
        token = generate_token(username)
        return jsonify({
            "message": "Login berhasil",
            "token": token,
            "username": username
        })
    else:
        return jsonify({"error": "Username atau password salah"}), 401
