from flask import Blueprint, jsonify, request
from models import Professional, db 
import jwt
from flask_bcrypt import Bcrypt
from . import bcrypt

professionalApi = Blueprint('professionalApi', __name__)

@professionalApi.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    founduser = Professional.query.filter_by(email=data['email']).first()
    if founduser:
        return jsonify({'message': 'User already exists'}), 409
    else:
        password = bcrypt.generate_password_hash(data['password']) 
        newuser = Professional(
            email=data['email'],
            username=data['username'],
            password=password,
            # serviceId=data['serviceId'],
            experience=data['experience'],
            contact=data['contact'],
            pincode=data['pincode']
        )
        db.session.add(newuser)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201