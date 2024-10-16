from flask import Blueprint, jsonify,request,current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import Services,ServiceImg,db
import os
import base64

adminApi = Blueprint('adminApi', __name__)

@adminApi.route('/', methods=['GET'])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        return jsonify({'message': 'You are an admin'}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 403


#********************** New Service Api******************************

# Create
@adminApi.route('/service', methods=['POST'])
def serviceCreate():
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'message': 'No data received'}), 400

        foundservice = Services.query.filter_by(serviceName=data['serviceName']).first()
        
        if foundservice:
            return jsonify({'message': 'Service already exists'}), 409
        
        newservice = Services(
            serviceName=data['serviceName'],
            description=data['description'],
            price=data['price']
        )
        db.session.add(newservice)
        db.session.commit()

        # Save image
        if 'ImgFilePath' in data:
            image_data = data['ImgFilePath'].split(',')[1]  
            try:
                image_bytes = base64.b64decode(image_data)
            except Exception as e:
                return jsonify({'message': 'Error decoding image data', 'error': str(e)}), 400
            
            filename = secure_filename(f"{newservice.id}_service_image.jpg")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)

            try:
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)

                service_img = ServiceImg(
                    name=filename,
                    filepath=filepath,
                    mimetype="image/jpeg", 
                    Service_id=newservice.id
                )
                db.session.add(service_img)
                db.session.commit()
            except Exception as e:
                return jsonify({'message': 'Error saving image', 'error': str(e)}), 500

        return jsonify({'message': 'Service created successfully'}), 201

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

