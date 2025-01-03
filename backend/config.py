import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVICE_IMAGE_FOLDER = os.path.join(os.getcwd(), 'static/services_imgs/')
    CUSTOMER_IMAGE_FOLDER = os.path.join(os.getcwd(), 'static/customers_imgs/') 
    PROFESSIONAL_IMAGE_FOLDER = os.path.join(os.getcwd(), 'static/professionals_imgs/')

    # Redis Configuration
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0 
        
    # Email Configuration for MailHog
    MAIL_SERVER = 'localhost'  
    MAIL_PORT = 1025           
    MAIL_USE_SSL = False       
    MAIL_USERNAME = None      
    MAIL_PASSWORD = None       
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')  
