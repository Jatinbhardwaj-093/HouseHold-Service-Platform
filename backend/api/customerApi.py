from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import func 

from models import Customer,CustomerImg, Services, ServiceImg,ServiceRequest,Professional,ServiceReview, db 
from . import bcrypt,custom_jwt_required,redis_client,get_token_expiration_time
from datetime import datetime, timedelta
import json
import os

customerApi = Blueprint('customerApi', __name__)


# ******************************Customer SIGNUP API****************************************
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
        
        redis_client.delete('admin:customers:all')
        return jsonify({'message': 'User created successfully'}), 201

# ******************************Customer HOME API****************************************

@customerApi.route('/', methods=['GET'])
@custom_jwt_required
def home():
    try:
        user = request.user
        founduser = Customer.query.filter_by(username=user).first()
        if founduser:
            cached_key = f'customer:{founduser.id}:details'
            cached_data = redis_client.get(cached_key)
            if cached_data:
                return jsonify(json.loads(cached_data)), 200

            # Fetch image details
            customer_image = CustomerImg.query.filter_by(Customer_id=founduser.id).first()
            if customer_image:
                image_name = f'{customer_image.name}'
            else:
                image_name = None

            # customer data
            customer = {
                'id': founduser.id,
                'password': '',
                'email': founduser.email,
                'username': founduser.username,
                'contact': founduser.contact,
                'pincode': founduser.pincode,
                'address': founduser.Address,
                'image_name': image_name,  
            }

            # response data
            response = {
                'customer': customer,
            }

            # Cache the response
            redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response))
            return jsonify(response), 200

        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500



# ******************************Customer PROFILE API****************************************

#Read
@customerApi.route('/profile', methods=['GET'])
@custom_jwt_required
def profile():
    try:
        user = request.user
        founduser = Customer.query.filter_by(username = user).first()
        if founduser:
            cached_key = f'customer:{founduser.id}:details'
            cached_data = redis_client.get(cached_key)
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
            
            image = CustomerImg.query.filter_by(Customer_id=founduser.id).first()
            if image:
                image_name = f'{image.name}'
            else:
                image_name = None
            
            customer = {
                'id': founduser.id,
                'password': '',
                'email': founduser.email,
                'username': founduser.username,
                'contact': founduser.contact,
                'pincode': founduser.pincode,
                'address': founduser.Address,
                'image_name': image_name
            }
            # response data
            response = {
                'customer': customer,
            }
            
            redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response))
            return jsonify(response), 200
            
        else:
            return jsonify({'message': 'User not found'}), 404   
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    
#Update
@customerApi.route('/profile', methods=['PUT'])
@custom_jwt_required
def updateProfile():
    user = request.user
    founduser = Customer.query.filter_by(username=user).first()
    if not founduser:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.form
    try:
        if 'password' in data and data['password']:
            password = bcrypt.generate_password_hash(data['password'])
            founduser.password = password
        
        founduser.username = data['username']
        founduser.email = data['email']
        founduser.contact = data['contact']
        founduser.pincode = data['pincode']
        founduser.Address = data['address']

        # Image Handling
        if 'image' in request.files:
            image_file = request.files['image']
            
            if image_file.filename:
                image_filename = secure_filename(f'Customer_{founduser.id}.jpg')
                
                # Create the directory if it doesn't exist
                if not os.path.exists(current_app.config['CUSTOMER_IMAGE_FOLDER']):
                    os.makedirs(current_app.config['CUSTOMER_IMAGE_FOLDER'])
                
                # Check file type
                ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
                if image_file.mimetype.split('/')[-1].lower() not in ALLOWED_EXTENSIONS:
                    return jsonify({'message': 'Invalid file type'}), 400

                # Delete existing image
                existing_image = CustomerImg.query.filter_by(Customer_id=founduser.id).first()
                if existing_image:
                    try:
                        os.remove(existing_image.filepath)
                    except OSError:
                        pass
                    db.session.delete(existing_image)

                # Save new image
                image_filepath = os.path.join(current_app.config['CUSTOMER_IMAGE_FOLDER'], image_filename)
                image_file.save(image_filepath)
                
                # Save the new image in the database
                new_image = CustomerImg(
                    name=image_filename,
                    filepath=image_filepath,
                    mimetype=image_file.mimetype,
                    Customer_id=founduser.id
                )
                db.session.add(new_image)
        db.session.commit()

        redis_client.delete(f'customer:{founduser.id}:details')
        redis_client.delete('admin:customers:all')
        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500  

# ******************************Customer SERVICE API****************************************

#Read
@customerApi.route('/services', methods=['GET'])
@custom_jwt_required
def services():
    try:
        cached_key = 'customer:services'
        cached_data = redis_client.get(cached_key)
        if cached_data:
            return jsonify(json.loads(cached_data)), 200

        services = Services.query.all()
        response = []
        for service in services:
            image = ServiceImg.query.filter_by(Service_id=service.id).first()
            response.append({
                'id': service.id,
                'name': service.serviceName,
                'description': service.description,
                'price': service.price,
                'image_name': image.name if image else None
            })
        
        redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response))
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


# ******************************CUSTOMER PARTICULAR SERVICE API****************************************

#Read
@customerApi.route('/service/<int:service_id>', methods=['GET'])
@custom_jwt_required
def service(service_id):
    try:
        cached_key = f'customer:service:{service_id}'
        cached_data = redis_client.get(cached_key)
        if cached_data:
            return jsonify(json.loads(cached_data)), 200
        
        service = Services.query.filter_by(id=service_id).first()
        if service:
            professionals = []
            for professional in service.professionals:
                professionals.append({
                    'professional_id': professional.id,
                    'professional_name': professional.username,
                    'professional_email': professional.email,
                    'professional_contact': professional.contact,
                    'professional_pincode': professional.pincode,
                    'professional_experience': professional.experience,
                    'professional_rating': professional.rating
                })
                
            response = {'service': {
                'id': service.id,
                'service_name': service.serviceName,
                'description': service.description,
                'price': service.price
            },
                'professionals': professionals}
            
            redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response)), 200
            return jsonify(response), 200
        else:
            return jsonify({'message': 'Service not found'}), 404

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    

# ******************************CUSTOMER SERVICE BOOKING API****************************************

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
            
            redis_client.delete(f'customer:{founduser.id}:service:bookings')
            redis_client.delete(f'professional:{data["professionalId"]}:service:requests')
            redis_client.delete('admin:ongoing_services:all')
            
            return jsonify({'message': 'Booking created successfully'}), 201
        else:
            return jsonify({'message': 'Service not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404

#Read
@customerApi.route('/service/bookings', methods=['GET'])
@custom_jwt_required
def serviceBookings():
    try:
        user = request.user
        founduser = Customer.query.filter_by(username = user).first()
        if founduser:
            cached_key = f'customer:{founduser.id}:service:bookings'
            cached_data = redis_client.get(cached_key)
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
            
            bookings = ServiceRequest.query.filter_by(customerId = founduser.id).all()
            response = []
            for booking in bookings:
                foundProfessional = Professional.query.filter_by(id = booking.professionalId).first()
                response.append({
                    'id': booking.id,
                    'serviceName': booking.service.serviceName,
                    'professionalName': foundProfessional.username,
                    'requestDate': booking.requestDate.isoformat(),
                    'completionDate': booking.completionDate.isoformat() if booking.completionDate else None,
                    'customerStatus': booking.customerStatus,
                    'professionalStatus': booking.professionalStatus,
                    'reviewed': booking.reviewed
                })

            redis_client.setex(cached_key, timedelta(minutes=15), json.dumps(response))
            return jsonify(response), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

#Update (Marking Complete)
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
            
            redis_client.delete(f'customer:{founduser.id}:service:bookings')
            redis_client.delete(f'professional:{booking.professionalId}:service:requests')
            redis_client.delete('admin:ongoing_services:all')
            
            return jsonify({'message': 'Booking updated successfully'}), 200
        else:
            return jsonify({'message': 'Booking not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    
#Update (Rescheduling)
@customerApi.route('/service/booking/<int:booking_id>/reschedule', methods=['PUT'])
@custom_jwt_required
def rescheduleServiceBooking(booking_id):
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:
        data = request.get_json()
        booking = ServiceRequest.query.filter_by(id = booking_id).first()
        if booking:
            booking.requestDate = datetime.strptime(data['serviceDate'], "%Y-%m-%d").date()
            db.session.commit()
            
            redis_client.delete(f'customer:{founduser.id}:service:bookings')
            redis_client.delete(f'professional:{booking.professionalId}:service:requests')
            redis_client.delete('admin:ongoing_services:all')
            
            return jsonify({'message': 'Booking rescheduled successfully'}), 200
        else:
            return jsonify({'message': 'Booking not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    
#Delete
@customerApi.route('/service/booking/<int:booking_id>/delete', methods=['DELETE'])
@custom_jwt_required
def deleteServiceBooking(booking_id):
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:
        booking = ServiceRequest.query.filter_by(id = booking_id).first()
        if booking:
            db.session.delete(booking)
            db.session.commit()
            
            redis_client.delete(f'customer:{founduser.id}:service:bookings')
            redis_client.delete(f'professional:{booking.professionalId}:service:requests')
            redis_client.delete('admin:ongoing_services:all')
            
            return jsonify({'message': 'Booking deleted successfully'}), 200
        else:
            return jsonify({'message': 'Booking not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    

# ***************************************** Service Review Api *************************************

#Create
@customerApi.route('/service/<int:booking_id>/review/create', methods=['POST'])
@custom_jwt_required
def serviceReview(booking_id):
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:
        data = request.get_json()
        booking = ServiceRequest.query.filter_by(id = booking_id).first()
        if booking:
            review = ServiceReview(
                ServiceRequestId = booking_id,
                serviceId = booking.serviceId,
                customerId = founduser.id,
                professionalId = booking.professionalId,
                rating = data['rating'],
                review = data['review']
            )
            
            updateReviewStatus = ServiceRequest.query.filter_by(id = booking_id).first()
            updateReviewStatus.reviewed = 'yes'
            
            db.session.add(review)
            db.session.commit()
            
            #updating professional rating
            update_professional_rating(booking.professionalId)
            
            redis_client.delete(f'customer:{founduser.id}:service:bookings')
            redis_client.delete(f'professional:{booking.professionalId}:service:requests:history')
            redis_client.delete(f'customer:professional:{booking.professionalId}:service:reviews')
            
            return jsonify({'message': 'Review created successfully'}), 201
        else:
            return jsonify({'message': 'Booking not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404

#Read
@customerApi.route('/professional/<int:professional_id>/reviews', methods=['GET'])
@custom_jwt_required
def professionalReviews(professional_id):
    try:
        cached_key = f'customer:professional:{professional_id}:service:reviews'
        cached_data = redis_client.get(cached_key)
        if cached_data:
            return jsonify(json.loads(cached_data)), 200
        reviews = ServiceReview.query.filter_by(professionalId = professional_id).all()
        response = []
        for review in reviews:
            customer = Customer.query.filter_by(id = review.customerId).first()
            response.append({
                'id': review.id,
                'customerName' : customer.username,
                'rating': review.rating,
                'review': review.review
            })
        
        redis_client.setex(cached_key, timedelta(minutes=5), json.dumps(response))
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


#Update
@customerApi.route('/service/<int:booking_id>/review/update', methods=['PUT'])
@custom_jwt_required
def updateServiceReview(booking_id):
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:
        data = request.get_json()
        review = ServiceReview.query.filter_by(ServiceRequestId = booking_id).first()
        if review:
            review.rating = data['rating']
            review.review = data['review']
            db.session.commit()
            
            #updating professional rating
            update_professional_rating(review.professionalId)
            
            redis_client.delete(f'customer:{founduser.id}:service:bookings')
            redis_client.delete(f'professional:{review.professionalId}:service:requests:history')
            redis_client.delete(f'customer:professional:{review.professionalId}:service:reviews')
            
            return jsonify({'message': 'Review updated successfully'}), 200
        else:
            return jsonify({'message': 'Review not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404
    
#Delete
@customerApi.route('/service/<int:booking_id>/review/delete', methods=['DELETE'])
@custom_jwt_required
def deleteServiceReview(booking_id):
    user = request.user
    founduser = Customer.query.filter_by(username = user).first()
    if founduser:
        review = ServiceReview.query.filter_by(ServiceRequestId = booking_id).first()
        service_request = ServiceRequest.query.filter_by(id = booking_id).first()
        if review:
            db.session.delete(review)
            service_request.reviewed = 'no'
            db.session.commit()
            
            #updating professional rating
            update_professional_rating(review.professionalId)
            
            redis_client.delete(f'customer:{founduser.id}:service:bookings')
            redis_client.delete(f'professional:{review.professionalId}:service:requests:history')
            redis_client.delete(f'customer:professional:{review.professionalId}:service:reviews')
            return jsonify({'message': 'Review deleted successfully'}), 200
        else:
            return jsonify({'message': 'Review not found'}), 404
    else:
        redis_delete('customer:service:bookings')
        return jsonify({'message': 'User not found'}), 404
    
    
# ******************************************************************************
#  update professional rating

def update_professional_rating(professional_id):
    avg_rating = db.session.query(func.avg(ServiceReview.rating)).filter(
        ServiceReview.professionalId == professional_id
    ).scalar()
    
    professional = Professional.query.get(professional_id)
    if professional:
        professional.rating = avg_rating if avg_rating else 0
        db.session.commit()
#******************************************************************************



# ***************************************** Customer Statistics Api *************************************

@customerApi.route('/statistics', methods=['GET'])
@custom_jwt_required
def getStatistics():
    try:
        user = request.user
        founduser = Customer.query.filter_by(username = user).first()
        if founduser:
            requested_services = (
            db.session.query(ServiceRequest.serviceId, func.count(ServiceRequest.id).label('requestCount'))
            .filter(ServiceRequest.customerId == founduser.id)
            .group_by(ServiceRequest.serviceId)
            .all()
            )
            
            services = ServiceRequest.query.filter_by(customerId = founduser.id).all()
            ServiceStatus = {
                'pending': 0,
                'completed': 0,
                'rejected': 0
            }

            for service in services:
                if service.professionalStatus == 'pending':
                    ServiceStatus['pending'] += 1
                elif service.professionalStatus == 'completed':
                    ServiceStatus['completed'] += 1
                elif service.professionalStatus == 'rejected':
                    ServiceStatus['rejected'] += 1
                
            service_data = [{'name': Services.query.get(service.serviceId).serviceName, 'requestCount': service.requestCount} for service in requested_services]

            response = {
                'AskedServices': service_data,
                'ServiceStatus': ServiceStatus
                
                }
            
            return response, 200
        else:
            return jsonify({'message': 'User not found'}), 404
        
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

# ***************************************** Logout Api *************************************

@customerApi.route('/logout', methods=['POST'])
@custom_jwt_required
def logout():
    try:
        user = request.user
        founduser = Customer.query.filter_by(username=user).first()
        
        if founduser:
            redis_client.delete(f'customer:{founduser.id}:details')
            redis_client.delete(f'customer:{founduser.id}:service:bookings')
            redis_client.delete(f'customer:{founduser.id}:service:reviews')
        
        authorization_header = request.headers.get('Authorization')
        if not authorization_header or not authorization_header.startswith('Bearer '):
            return jsonify({'message': 'Authorization header is missing or invalid'}), 400
        
        token = authorization_header.split(' ')[1]
        if token:
            expiration_time = get_token_expiration_time(token)  
            redis_client.setex(f'blacklisted_token:{token}', expiration_time, 'blacklisted')

            return jsonify({'message': 'Logout successful'}), 200

        return jsonify({'message': 'Token not found'}), 400

    except Exception as e:
        current_app.logger.error(f"Error during logout: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500
    
    
    

