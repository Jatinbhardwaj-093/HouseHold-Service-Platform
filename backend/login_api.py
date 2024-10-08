from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import bcrypt


jwt = JWTManager(app)

CORS(app)

# A mock database of users (username: hashed_password)
users = {
    "testuser": bcrypt.hashpw("testpassword".encode('utf-8'), bcrypt.gensalt()),
    "admin": bcrypt.hashpw("adminpassword".encode('utf-8'), bcrypt.gensalt())
}

# Route for login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users:
        # Check the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), users[username]):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Bad username or password"}), 401
    else:
        return jsonify({"msg": "Bad username or password"}), 401

# A protected route to verify token
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

