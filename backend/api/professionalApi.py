from flask import Blueprint, jsonify, request
from models import Professional, db ,Services,ServiceRequest, ServiceImg, ServiceReview, Customer
import jwt
from flask_bcrypt import Bcrypt
from . import bcrypt,custom_jwt_required,redis_client
from datetime import datetime, timedelta
from sqlalchemy import func
import json

professionalApi = Blueprint('professionalApi', __name__)


# ******************************Professional SIGNUP API****************************************
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
        redis_client.delete('admin:professionals:all')
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

# ******************************Professional HOME API****************************************
@professionalApi.route('/', methods=['GET'])
@custom_jwt_required
def home():
    try:
        user = request.user
        founduser = Professional.query.filter_by(username = user).first()
        if founduser:
            cached_key = f'professional:{founduser.id}:details'
            cached_data = redis_client.get(cached_key)
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
            
            response = {
                'id': founduser.id,
                'username': founduser.username,
                'password': '',
                'email': founduser.email,
                'contact': founduser.contact,
                'experience': founduser.experience,
                'pincode': founduser.pincode,
                'serviceType': founduser.serviceType.serviceName
            }
            redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response))
            return jsonify(response), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
        
    
# ******************************Professional PROFILE API****************************************

#Read
@professionalApi.route('/profile', methods=['GET'])
@custom_jwt_required
def profile():
    try:
        user = request.user
        founduser = Professional.query.filter_by(username = user).first()
        if founduser:
            cached_key = f'professional:{founduser.id}:details'
            cached_data = redis_client.get(cached_key)
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
        
            response = {
                'id': founduser.id,
                'username': founduser.username,
                'password': '',
                'email': founduser.email,
                'contact': founduser.contact,
                'experience': founduser.experience,
                'pincode': founduser.pincode,
                'serviceType': founduser.serviceType.serviceName
            }
            redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response))
            return jsonify(response), 200
            
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    
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
        
        redis_client.delete(f'professional:{founduser.id}:details')
        redis_client.delete('admin:professionals:all')
        return jsonify({'message': 'Profile updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
# ******************************Professional SERVICE REQUESTS API****************************************

#Read
@professionalApi.route('/service/requests', methods=['GET'])
@custom_jwt_required
def serviceRequests():
    try:
        user = request.user
        founduser = Professional.query.filter_by(username = user).first()
        if founduser:
            cached_key = f'professional:{founduser.id}:service:requests'
            cached_data = redis_client.get(cached_key)
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
            
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
                    'requestDate': serviceRequest.requestDate.isoformat() if serviceRequest.completionDate else None,
                    'completionDate': serviceRequest.completionDate.isoformat() if serviceRequest.completionDate else None,
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
            redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response))
            return jsonify(response), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    
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
            
            redis_client.delete(f'professional:{founduser.id}:service:requests')
            redis_client.delete(f'customer:{booking.customerId}:service:bookings')
            redis_client.delete('admin:ongoing_services:all')
            
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
            
            redis_client.delete(f'professional:{founduser.id}:service:requests')
            redis_client.delete(f'customer:{booking.customerId}:service:bookings')
            redis_client.delete('admin:ongoing_services:all')
            
            return jsonify({'message': 'Booking updated successfully'}), 200
        else:
            return jsonify({'message': 'Booking not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    
    
# ******************************Customer SERVICE REQUESTS API****************************************

#Read
@professionalApi.route('/service/requests/history', methods=['GET'])
@custom_jwt_required
def serviceRequestHistory():
    try:
        user = request.user
        founduser = Professional.query.filter_by(username = user).first()
        if founduser:
            cached_key = f'professional:{founduser.id}:service:requests:history'
            cached_data = redis_client.get(cached_key)
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
            
            requests = ServiceRequest.query.filter_by(professionalId = founduser.id).all()
            response = []
            for serviceRequest in requests:
                foundCustomer = Customer.query.filter_by(id = serviceRequest.customerId).first()
                foundReview = ServiceReview.query.filter_by(ServiceRequestId = serviceRequest.id).first()
                data = {
                    'id': serviceRequest.id,
                    'customerId': serviceRequest.customerId,
                    'customerName': foundCustomer.username,
                    'customerAddress': foundCustomer.Address,
                    'customerContact': foundCustomer.contact,
                    'customerPincode': foundCustomer.pincode,
                    'requestDate': serviceRequest.requestDate.isoformat() if serviceRequest.completionDate else None,
                    'completionDate': serviceRequest.completionDate.isoformat() if serviceRequest.completionDate else None,
                    'customerStatus': serviceRequest.customerStatus,
                    'professionalStatus': serviceRequest.professionalStatus,
                    'reviewed': serviceRequest.reviewed,
                    'rating': foundReview.rating if foundReview else None,
                    'review': foundReview.review if foundReview else None
                }
                response.append(data)
            
            redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response))
            return jsonify(response), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    
# ******************************STATISTICS API****************************************
@professionalApi.route('/statistics', methods=['GET'])
@custom_jwt_required
def statistics():
    user = request.user
    founduser = Professional.query.filter_by(username=user).first()
    
    if founduser:
        services = ServiceRequest.query.filter_by(professionalId=founduser.id).all()
        serviceStatus = {
            'pending': 0,
            'completed': 0,
            'rejected': 0
        }

        for service in services:
            if service.professionalStatus == 'pending':
                serviceStatus['pending'] += 1
            elif service.professionalStatus == 'completed':
                serviceStatus['completed'] += 1
            elif service.professionalStatus == 'rejected':
                serviceStatus['rejected'] += 1
        
        results = (
            db.session.query(
                Customer.pincode,  
                func.count(ServiceRequest.id).label('request_count')  
            )
            .join(ServiceRequest, ServiceRequest.customerId == Customer.id)  
            .group_by(Customer.pincode)  
            .all()  
        )

        differentPincode = [
            {'pincode': row.pincode, 'requestCount': row.request_count} 
            for row in results
        ]
        
        requestDates = {}
        for service in services:
            if str(service.requestDate) not in requestDates:
                requestDates[str(service.requestDate)] = 1
            else:
                requestDates[str(service.requestDate)] += 1

        response = {
            'ServiceStatus': serviceStatus,
            'DifferentPincode': differentPincode,
            'requestDates' : requestDates
        }

        return jsonify(response), 200
    else:
        return jsonify({'message': 'User not found'}), 404
