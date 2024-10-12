from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

adminApi = Blueprint('adminApi', __name__)

@adminApi.route('/', methods=['GET'])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        return jsonify({'message': 'You are an admin'}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 403
