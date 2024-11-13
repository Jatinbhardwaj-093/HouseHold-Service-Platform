from flask import Blueprint, jsonify,request,current_app
from werkzeug.utils import secure_filename
from models import Services,ServiceImg,Customer,Professional,ServiceRequest,ServiceReview,db
from . import bcrypt,custom_jwt_required
import os
import base64

adminApi = Blueprint('adminApi', __name__)



#********************** Admin Home Api******************************

@adminApi.route('/', methods=['GET', 'OPTIONS'])

def home():
    print('Authorization Header:', request.headers.get('Authorization'))  # Check if JWT is received
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


#********************** New Service Api******************************

# Create
@adminApi.route('/service', methods=['POST'])
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

    return jsonify({'message': 'Service created successfully', 'service_id': new_service.id}), 201

#Read
@adminApi.route('/service/<int:service_id>', methods=['GET'])
def read_service(service_id):
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

    return jsonify(service_data), 200

# Update
@adminApi.route('/service/<int:service_id>', methods=['PUT'])
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

        # Delete the old image
        existing_image = ServiceImg.query.filter_by(Service_id=service.id).first()
        if existing_image:
            os.remove(existing_image.filepath)  
            db.session.delete(existing_image)

        # Save the new image
        filename = secure_filename(image.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)


        new_image = ServiceImg(name=filename, filepath=filepath, mimetype=image.mimetype, Service_id=service.id)
        db.session.add(new_image)

    db.session.commit()
    return jsonify({'message': 'Service updated successfully'}), 200


#Delete
@adminApi.route('/service/<int:service_id>', methods=['DELETE'])
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

    return jsonify({'message': 'Service and associated image deleted successfully'}), 200


# Admin Customers Api

#Read
@adminApi.route('/customers', methods=['GET'])
def customers():
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
    return jsonify(response), 200

#Update(Flag)
@adminApi.route('/customer/<int:customer_id>/flag', methods=['PUT'])
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
    return jsonify({'message': 'Customer updated successfully'}), 200   

#Delete
@adminApi.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

#Admin Professional Api

#Read
@adminApi.route('/professional', methods=['GET'])
@custom_jwt_required
def professionals():
    
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
    return jsonify(response), 200

#Update(Flag)
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
    return jsonify({'message': 'Professional updated successfully'}), 200


#Update(Verify)
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
    return jsonify({'message': 'Professional deleted successfully'}), 200

#Admin OngoingService Api

#Read
@adminApi.route('/ongoingServices', methods=['GET'])
@custom_jwt_required
def ongoingServices():
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
            'requestDate': ongoingService.requestDate,
            'completionDate': ongoingService.completionDate
            
        })
    return jsonify(response), 200