from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from models import Services, ServiceImg, Customer, Professional, ServiceRequest, ServiceReview, db
from . import bcrypt, custom_jwt_required,redis_client
import os
import base64
from sqlalchemy import func
from datetime import timedelta
import json

adminApi = Blueprint('adminApi', __name__)

# ******************* Admin Home Api ***************
@adminApi.route('/', methods=['GET'])
@custom_jwt_required
def home():
    try:
        cache_key = 'admin:services:all'
        cached_data = redis_client.get(cache_key)
        
        if cached_data:
            return jsonify(json.loads(cached_data)), 200

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
        
        redis_client.setex(cache_key, timedelta(minutes=15), json.dumps(response))
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


# ******************* Admin Service Api ***************

#Create

@adminApi.route('/service', methods=['POST'])
@custom_jwt_required
def create_service():
    data = request.get_json()
    
    new_service = Services(
        serviceName=data['serviceName'],
        description=data['description'],
        price=data['price']
    )
    db.session.add(new_service)
    db.session.commit()

    if 'image' in request.files:
        image_file = request.files['image']
        original_image_path = os.path.join(current_app.config['UPLOAD_FOLDER)'], image_file.filename)
        compressed_image_path = os.path.join(current_app.config['UPLOAD_FOLDER)'], 'compressed_' + image_file.filename)

        image_file.save(original_image_path)  
        compress_image(original_image_path, compressed_image_path) 
        
        service_image = ServiceImg(
            name=image_file.filename,
            filepath=compressed_image_path,
            mimetype=image_file.content_type,
            Service_id=new_service.id
        )
        db.session.add(service_image)
        db.session.commit()
    
    redis_client.delete('admin:services:all')
    return jsonify({'message': 'Service created successfully', 'service_id': new_service.id}), 201

#Read
@adminApi.route('/service/<int:service_id>', methods=['GET'])
@custom_jwt_required
def read_service(service_id):
    cache_key = f'admin:service:{service_id}'
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return jsonify(json.loads(cached_data)), 200
        
    service = Services.query.filter_by(id=service_id).first()
    
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    service_img = ServiceImg.query.filter_by(Service_id=service.id).first()
    
    service_data = {
        'service_id': service.id,
        'service_name': service.serviceName,
        'description': service.description,
        'price': service.price,
        'image': {
            'name': service_img.name if service_img else None,
            'filepath': service_img.filepath if service_img else None,
            'mimetype': service_img.mimetype if service_img else None
        }
    }
    
    redis_client.setex(cache_key, timedelta(minutes=15), json.dumps(service_data))
    return jsonify(service_data), 200

#Update
@adminApi.route('/service/<int:service_id>', methods=['PUT'])
@custom_jwt_required
def edit_service(service_id):
    service = Services.query.filter_by(id=service_id).first()
    
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    data = request.get_json()

    service.serviceName = data['service_name']
    service.description = data['description']
    service.price = data['price']

    if 'image' in request.files:
        image = request.files['image']
        existing_image = ServiceImg.query.filter_by(Service_id=service.id).first()
        if existing_image:
            os.remove(existing_image.filepath)  
            db.session.delete(existing_image)

        filename = secure_filename(image.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        new_image = ServiceImg(name=filename, filepath=filepath, mimetype=image.mimetype, Service_id=service.id)
        db.session.add(new_image)

    db.session.commit()
    redis_client.delete(f'admin:service:{service_id}')
    redis_client.delete('admin:services:all')
    return jsonify({'message': 'Service updated successfully'}), 200


#Delete
@adminApi.route('/service/<int:service_id>', methods=['DELETE'])
@custom_jwt_required
def delete_service(service_id):
    service = Services.query.get(service_id)
    
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    service_img = ServiceImg.query.filter_by(Service_id=service_id).first()

    if service_img:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], service_img.filepath)
        if os.path.exists(image_path):
            os.remove(image_path) 
        db.session.delete(service_img)

    db.session.delete(service)
    db.session.commit()
    
    redis_client.delete(f'admin:service:{service_id}')
    redis_client.delete('admin:services:all')
    return jsonify({'message': 'Service and associated image deleted successfully'}), 200


#******************* Admin Customer Api ***************

#Read
@adminApi.route('/customers', methods=['GET'])
@custom_jwt_required
def customers():
    cache_key = 'admin:customers:all'
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return jsonify(json.loads(cached_data)), 200
        
    customers = Customer.query.all()
    response = []
    for customer in customers:
        response.append({
            'id': customer.id,
            'email': customer.email,
            'username': customer.username,
            'contact': customer.contact,
            'pincode': customer.pincode,
            'address': customer.Address,
            'flag': customer.flag
        })
    
    redis_client.setex(cache_key, timedelta(minutes=15), json.dumps(response))
    return jsonify(response), 200

#Update
@adminApi.route('/customer/<int:customer_id>/flag', methods=['PUT'])
@custom_jwt_required
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    data = request.get_json()
    if customer.flag == 'yes':
        customer.flag = 'no'
    else:
        customer.flag = 'yes'
    db.session.commit()
    redis_client.delete('admin:customers:all')
    return jsonify({'message': 'Customer updated successfully'}), 200   

#Delete
@adminApi.route('/customer/<int:customer_id>', methods=['DELETE'])
@custom_jwt_required
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    redis_client.delete('admin:customers:all')
    return jsonify({'message': 'Customer deleted successfully'}), 200


#******************* Admin Professional Api ***************

#Read
@adminApi.route('/professional', methods=['GET'])
@custom_jwt_required
def professionals():
    cache_key = 'admin:professionals:all'
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return jsonify(json.loads(cached_data)), 200
        
    professionals = Professional.query.all()
    response = []
    for professional in professionals:
        response.append({
            'professionalId': professional.id,
            'email': professional.email,
            'username': professional.username,
            'pincode': professional.pincode,
            'serviceId': professional.serviceId,
            'serviceName': professional.serviceType.serviceName,
            'rating': professional.rating,
            'experience': professional.experience,
            'flag': professional.flag,
            'verify': professional.verify
        })
    
    redis_client.setex(cache_key, timedelta(minutes=15), json.dumps(response))
    return jsonify(response), 200

#Update
@adminApi.route('/professional/<int:professional_id>/flag', methods=['PUT'])
@custom_jwt_required
def update_professional(professional_id):
    professional = Professional.query.get(professional_id)  
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    data = request.get_json()
    if professional.flag == 'yes':
        professional.flag = 'no'
    else:
        professional.flag = 'yes'
    db.session.commit()
    redis_client.delete('admin:professionals:all')
    return jsonify({'message': 'Professional updated successfully'}), 200

#Update
@adminApi.route('/professional/<int:professional_id>/verify', methods=['PUT'])
@custom_jwt_required
def update_professional_verify(professional_id):
    professional = Professional.query.get(professional_id)  
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    data = request.get_json()
    if professional.verify == 'yes':
        professional.verify = 'no'
    else:
        professional.verify = 'yes'
    db.session.commit()
    redis_client.delete('admin:professionals:all')
    return jsonify({'message': 'Professional updated successfully'}), 200

#Delete
@adminApi.route('/professional/<int:professional_id>/delete', methods=['DELETE'])
@custom_jwt_required
def delete_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({'error': 'Professional not found'}), 404
    db.session.delete(professional)
    db.session.commit()
    redis_client.delete('admin:professionals:all')
    return jsonify({'message': 'Professional deleted successfully'}), 200


#******************* Admin Service Api ***************

#Read
@adminApi.route('/ongoingServices', methods=['GET'])
@custom_jwt_required
def ongoingServices():
    cache_key = 'admin:ongoing_services:all'
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return jsonify(json.loads(cached_data)), 200
        
    ongoingServices = ServiceRequest.query.all()
    response = []
    for ongoingService in ongoingServices:
        customer = Customer.query.filter_by(id = ongoingService.customerId).first()
        professional = Professional.query.filter_by(id = ongoingService.professionalId).first()
        response.append({
            'bookingId': ongoingService.id,
            'customerName': customer.username,
            'professionalName': professional.username,
            'customerPincode': customer.pincode,
            'professionalPincode': professional.pincode,
            'serviceName': ongoingService.service.serviceName,
            'serviceId': ongoingService.serviceId,
            'status': ongoingService.professionalStatus,
            'requestDate': ongoingService.requestDate.isoformat() ,
            'completionDate': ongoingService.completionDate.isoformat() if ongoingService.completionDate else None
            })

    
    redis_client.setex(cache_key, timedelta(minutes=5), json.dumps(response))
    return jsonify(response), 200


# ******************* Admin Statistics Api ***************
@adminApi.route('/statistics', methods=['GET'])
@custom_jwt_required
def statistics():
    ratio = {
        'Customer': db.session.query(Customer.id).count(),
        'Professional': db.session.query(Professional.id).count()
    }
    services = ServiceRequest.query.all()
    
    requestsOnDay = {}
    completionOnDay = {}
    for service in services:
        if str(service.requestDate) in requestsOnDay:
            requestsOnDay[str(service.requestDate)] += 1
        else:
            requestsOnDay[str(service.requestDate)] = 1
            
        if not service.completionDate:
            continue
        elif str(service.completionDate) in completionOnDay:
            completionOnDay[str(service.completionDate)] += 1
        else:
            completionOnDay[str(service.completionDate)] = 1
        
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

    response = {
        'ratioOfUsers': ratio,
        'requestsOnDay': requestsOnDay,
        'completionOnDay': completionOnDay,
        'serviceStatus': serviceStatus,
    }
    
    return jsonify(response), 200