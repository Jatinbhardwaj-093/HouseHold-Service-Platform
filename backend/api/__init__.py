# api/__init__.py
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import jwt  
from functools import wraps
from os import getenv
from datetime import datetime, timezone
import redis
from config import Config


bcrypt = Bcrypt()
jwt_manager = JWTManager()

redis_client = None
# Initialize Redis client
try:
        redis_client = redis.StrictRedis(
            host=Config.REDIS_HOST,        
            port=Config.REDIS_PORT,        
            db=Config.REDIS_DB,           
            decode_responses=True,  
            socket_timeout=5              
        )
        redis_client.ping()
except Exception as e:
    print(f"Redis connection failed: {str(e)}")
    redis_client = None

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

# expiration time of token for blacklist in logout
def get_token_expiration_time(token: str):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        exp_time = decoded_token.get('exp')
    
        if exp_time:
            return exp_time
        
        raise ValueError("Expiration time not found in token.")
    
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.DecodeError:
        raise ValueError("Error decoding the token.")
    except Exception as e:
        raise ValueError(f"Error retrieving expiration time: {str(e)}")

