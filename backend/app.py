from flask import Flask
from flask_migrate import Migrate
from models import db 
from flask_cors import CORS
#Api Imports
from api.loginApi import loginApi  
from api.customerApi import customerApi
from api.professionalApi import professionalApi
from api.adminApi import adminApi
#congig imports
from config import Config 
#bcrypt and jwt instance importing
from api import bcrypt,jwt_manager




def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(Config)

    bcrypt.init_app(app)  #Intialize bcrypt hashing library
    db.init_app(app)  # Initialize the db with the app
    jwt_manager.init_app(app)  # Initialize the JWT library
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    app.register_blueprint(loginApi)  # Register the login API
    app.register_blueprint(customerApi, url_prefix='/customer')  # Register the customer API
    app.register_blueprint(professionalApi, url_prefix='/professional')  # Register the professional API
    app.register_blueprint(adminApi, url_prefix='/admin')  # Register the admin API

    return app
