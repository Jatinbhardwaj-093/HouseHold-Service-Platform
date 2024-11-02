from flask import Blueprint, jsonify, request
from models import Professional, db ,Services, ServiceImg
import jwt
from flask_bcrypt import Bcrypt
from . import bcrypt,custom_jwt_required

professionalApi = Blueprint('professionalApi', __name__)

@professionalApi.route('/signup', methods=['POST'])
def signup():
    user = request.get_json()['username']
    founduser = Professional.query.filter_by(username = user).first()
    serviceType = request.get_json()['serviceType']
    foundService = Services.query.filter_by(serviceName = serviceType).first()
    if founduser:
        return jsonify({'message': 'User already exists'}), 409
    elif not foundService:
        return jsonify({'message': 'Service not found'}), 404
    else:
        data = request.get_json()
        password = bcrypt.generate_password_hash(data['password']) 
        newuser = Professional(
            email=data['email'],
            username=data['username'],
            password=password,
            serviceId=foundService.id,
            experience=data['experience'],
            contact=data['contact'],
            pincode=data['pincode']
        )
        db.session.add(newuser)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201


@professionalApi.route('/services', methods=['GET'])
def get_services():
    services = Services.query.all()
    response = []
    for service in services:
        response.append({
            'id': service.id,
            'name': service.serviceName,
            'description': service.description,
            'price': service.price
        })
    return jsonify(response), 200
    
@professionalApi.route('/', methods=['GET'])
def home():
    print('Authorization Header:', request.headers.get('Authorization')) 
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight response'}), 200

    try:
        services = Services.query.all()
        response = []

        for service in services:
            img = ServiceImg.query.filter_by(Service_id=service.id).first()
            response.append({
                'id': service.id,
                'description': service.description,
                'price': service.price,
                'name': service.serviceName,
                'image': img.filepath if img else None
            })
        return jsonify(response), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'An error occurred'}), 500