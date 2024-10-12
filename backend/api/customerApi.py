from flask import Blueprint, jsonify, request
from models import Customer, db 
from flask_jwt_extended import jwt_required,get_jwt_identity
from . import bcrypt

customerApi = Blueprint('customerApi', __name__)

@customerApi.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    founduser = Customer.query.filter_by(email=data['email']).first()
    if founduser:
        return jsonify({'message': 'User already exists'}), 409
    else:
        password = bcrypt.generate_password_hash(data['password']) 
        newuser = Customer(
            email=data['email'],
            username=data['username'],
            password=password,
            contact=data['contact'],
            pincode=data['pincode'],
            Address=data['Address']
        )
        db.session.add(newuser)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    