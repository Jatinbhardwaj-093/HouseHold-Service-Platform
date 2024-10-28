# api/__init__.py
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import jwt  
from functools import wraps
from os import getenv
from datetime import datetime, timezone


bcrypt = Bcrypt()
jwt_manager = JWTManager()

def custom_jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token_parts = auth_header.split()

            if len(token_parts) == 2 and token_parts[0] == "Bearer":
                token = token_parts[1]

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            payload = jwt.decode(token, getenv('SECRET_KEY'), algorithms=["HS256"])

            if datetime.fromtimestamp(payload['exp'], tz=timezone.utc) < datetime.now(tz=timezone.utc):
                return jsonify({"message": "Token has expired"}), 401
            
            request.user = payload['user']
            request.role = payload['role']

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function

