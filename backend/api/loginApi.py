from flask import Blueprint, jsonify, request
from models import Admin, Customer, Professional, db  
import datetime
import jwt
from os import getenv
from . import bcrypt

loginApi = Blueprint('loginApi', __name__)

def create_jwt_token(data):
    payload = {
        'user': data['username'],
        'role': data['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1) 
    }
    token = jwt.encode(payload, getenv('SECRET_KEY'), algorithm='HS256')
    return token

@loginApi.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    role = data['role']
    username = data['username']
    password = data['password']

    if role == 'admin':
        found_user = Admin.query.filter_by(username=username).first()
    elif role == 'professional':
        found_user = Professional.query.filter_by(username=username).first()
    elif role == 'customer':
        found_user = Customer.query.filter_by(username=username).first()
    else:
        return jsonify({'message': 'Invalid role'}), 401

    if found_user and bcrypt.check_password_hash(found_user.password,password):
        token_data = {
            'username': found_user.username,
            'role': role  
        }
        token = create_jwt_token(token_data)
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
