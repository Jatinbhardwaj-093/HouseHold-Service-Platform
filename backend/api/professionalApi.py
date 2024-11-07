from flask import Blueprint, jsonify, request
from models import Professional, db ,Services,ServiceRequest, ServiceImg,Customer
import jwt
from flask_bcrypt import Bcrypt
from . import bcrypt,custom_jwt_required
from datetime import datetime

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

# Professional Home Api
@professionalApi.route('/', methods=['GET'])
@custom_jwt_required
def home():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight response'}), 200

    try:
        user = request.user
        founduser = Professional.query.filter_by(username = user).first()
        if founduser:
            response = {
                'id': founduser.id,
                'username': founduser.username,
                'password': '',
                'email': founduser.email,
                'contact': founduser.contact,
                'experience': founduser.experience,
                'pincode': founduser.pincode
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'An error occurred'}), 500
    
# Professional Profile Api

#Read

@professionalApi.route('/profile', methods=['GET'])
@custom_jwt_required
def profile():
    user = request.user
    founduser = Professional.query.filter_by(username = user).first()
    
    if founduser:
        return jsonify({
            'id': founduser.id,
            'email': founduser.email,
            'username': founduser.username,
            'contact': founduser.contact,
            'pincode': founduser.pincode,
            'serviceType': founduser.serviceType.serviceName,
            'experience': founduser.experience
        }), 200
        
    else:
        return jsonify({'message': 'User not found'}), 404
    
#Update
@professionalApi.route('/profile', methods=['PUT'])
@custom_jwt_required
def updateProfile():
    user = request.user
    founduser = Professional.query.filter_by(username = user).first()
    if founduser:   
        data = request.get_json()
        password = bcrypt.generate_password_hash(data['password'])
        founduser.username = data['username']
        founduser.email = data['email']
        founduser.password = password
        founduser.contact = data['contact']
        founduser.pincode = data['pincode']
        founduser.experience = data['experience']
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
#Professional Services Request Api

#Read
@professionalApi.route('/service/requests', methods=['GET'])
@custom_jwt_required
def serviceRequests():
    user = request.user
    founduser = Professional.query.filter_by(username = user).first()
    if founduser:
        requests = ServiceRequest.query.filter_by(professionalId = founduser.id).all()
        newRequests = []
        ongoingRequests = []
        for serviceRequest in requests:
            foundCustomer = Customer.query.filter_by(id = serviceRequest.customerId).first()
            data = {
                'id': serviceRequest.id,
                'customerId': serviceRequest.customerId,
                'customerName': foundCustomer.username,
                'customerAddress': foundCustomer.Address,
                'customerContact': foundCustomer.contact,
                'customerPincode': foundCustomer.pincode,
                'requestDate': serviceRequest.requestDate,
                'completionDate': serviceRequest.completionDate,
                'customerStatus': serviceRequest.customerStatus,
                'professionalStatus': serviceRequest.professionalStatus
            }
            if serviceRequest.professionalStatus == 'pending':
                newRequests.append(data)
            elif serviceRequest.professionalStatus == 'accepted':
                ongoingRequests.append(data)
        response = {
            'newRequests': newRequests,
            'ongoingRequests': ongoingRequests
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
#Update Service Booking
@professionalApi.route('/service/request/<int:booking_id>', methods=['PUT'])
@custom_jwt_required
def updateServiceBooking(booking_id):
    user = request.user
    founduser = Professional.query.filter_by(username = user).first()
    if founduser:
        data = request.get_json()
        booking = ServiceRequest.query.filter_by(id = booking_id).first()
        if booking:
            if data['professionalStatus'] == 'accepted':
                booking.customerStatus = 'Pending'
            booking.professionalStatus = data['professionalStatus']    
            db.session.commit()
            return jsonify({'message': 'Booking updated successfully'}), 200
        else:
            return jsonify({'message': 'Booking not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    
#Update Service Completion
@professionalApi.route('/service/request/<int:booking_id>/complete', methods=['PUT'])
@custom_jwt_required
def updateServiceCompletion(booking_id):
    user = request.user
    founduser = Professional.query.filter_by(username = user).first()
    if founduser:
        data = request.get_json()
        booking = ServiceRequest.query.filter_by(id = booking_id).first()
        if booking:
            booking.completionDate = datetime.strptime(data['completionDate'], "%Y-%m-%d").date()
            booking.professionalStatus = 'completed'
            db.session.commit()
            return jsonify({'message': 'Booking updated successfully'}), 200
        else:
            return jsonify({'message': 'Booking not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404