from flask import Blueprint, jsonify, request
from models import Customer, Services, ServiceImg,ServiceRequest,Professional, db 
from . import bcrypt,custom_jwt_required
from datetime import datetime

customerApi = Blueprint('customerApi', __name__)

@customerApi.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    founduser = Customer.query.filter_by(username = data['username']).first()
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
            Address=data['address']
        )
        db.session.add(newuser)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

# Customer Home Api

@customerApi.route('/', methods=['GET'])
@custom_jwt_required
def home():
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:
        # customer details
        customer = {
            'password': '',
            'email': founduser.email,
            'username': founduser.username,
            'contact': founduser.contact,
            'pincode': founduser.pincode,
            'address': founduser.Address
        }
        
        # customer service bookings
        bookings = ServiceRequest.query.filter_by(customerId = founduser.id).all()
        service_bookings = []
        for booking in bookings:
            foundProfessional = Professional.query.filter_by(id = booking.professionalId).first()
            service_bookings.append({
                'id': booking.id,
                'serviceName': booking.service.serviceName,
                'professionalName': foundProfessional.username,
                'requestDate': booking.requestDate,
                'completionDate': booking.completionDate,
                'customerStatus': booking.customerStatus,
                'professionalStatus': booking.professionalStatus
            })

        # response data
        response = {
            'customer': customer,
            'service_bookings': service_bookings
        }
        
        return jsonify(response), 200

    else:
        return jsonify({'message': 'User not found'}), 404

# Customer Profile Api

#Read
@customerApi.route('/profile', methods=['GET'])
@custom_jwt_required
def profile():
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    
    if founduser:
        return jsonify({
            'id': founduser.id,
            'email': founduser.email,
            'username': founduser.username,
            'contact': founduser.contact,
            'pincode': founduser.pincode,
            'address': founduser.Address
        }), 200
        
    else:
        return jsonify({'message': 'User not found'}), 404   
    
#Update
@customerApi.route('/profile', methods=['PUT'])
@custom_jwt_required
def updateProfile():
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:    
        data = request.get_json()
        password = bcrypt.generate_password_hash(data['password'])
        founduser.username = data['username']
        founduser.email = data['email']
        founduser.password = password
        founduser.contact = data['contact']
        founduser.pincode = data['pincode']
        founduser.Address = data['address']
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404  

#Customer Services Api

#Read
@customerApi.route('/services', methods=['GET'])
@custom_jwt_required
def services():
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


# Customer Particular Service Api

#Read
@customerApi.route('/service/<int:service_id>', methods=['GET'])
@custom_jwt_required
def service(service_id):
    service = Services.query.filter_by(id=service_id).first()
    if service:
        response = []
        for professional in service.professionals:
            response.append({
                'professional_id': professional.id,
                'professional_name': professional.username,
                'professional_email': professional.email,
                'professional_contact': professional.contact,
                'professional_pincode': professional.pincode,
                'professional_experience': professional.experience,
                'professional_rating': professional.rating
            })
        return jsonify({
            'service': {
                'id': service.id,
                'service_name': service.serviceName,
                'description': service.description,
                'price': service.price
            },
            'professionals': response
        }), 200
    else:
        return jsonify({'message': 'Service not found'}), 404

# Customer Service Booking Api

#Create
@customerApi.route('/service/<int:service_id>/booking', methods=['POST'])
@custom_jwt_required
def serviceBooking(service_id):
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:
        data = request.get_json()
        service = Services.query.filter_by(id = service_id).first()
        if service:
            booking = ServiceRequest(
                customerId = founduser.id,
                serviceId = service_id,
                professionalId = data['professionalId'],
                requestDate = datetime.strptime(data['serviceDate'], "%Y-%m-%d").date()
            )
            db.session.add(booking)
            db.session.commit()
            return jsonify({'message': 'Booking created successfully'}), 201
        else:
            return jsonify({'message': 'Service not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    
#Update
@customerApi.route('/service/booking/<int:booking_id>/complete', methods=['PUT'])
@custom_jwt_required
def updateServiceBooking(booking_id):
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:
        data = request.get_json()
        booking = ServiceRequest.query.filter_by(id = booking_id).first()
        if booking:
            booking.completionDate = datetime.strptime(data['completionDate'], "%Y-%m-%d").date()
            booking.customerStatus = 'completed'
            db.session.commit()
            return jsonify({'message': 'Booking updated successfully'}), 200
        else:
            return jsonify({'message': 'Booking not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404