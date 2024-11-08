from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()  

class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username= db.Column(db.String, nullable=False)
    password= db.Column(db.String, nullable=False)

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email= db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    Address= db.Column(db.String, nullable=False)
    flag = db.Column(db.String, default='no')
    
class Professional(db.Model):
    __tablename__ = 'Professional'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    serviceId = db.Column(db.Integer, db.ForeignKey('Services.id'))
    experience = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.String, default='no')
    verify = db.Column(db.String, default='no')
    rating = db.Column(db.Integer, nullable=False, default=0)

    serviceType = db.relationship('Services', backref='professionals', lazy=True)

class Services(db.Model):
    __tablename__ = 'Services'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serviceName = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.String)

class ServiceImg(db.Model):
    __tablename__ = 'ServiceImg'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    Service_id = db.Column(db.Integer, db.ForeignKey('Services.id'))  
    
class ServiceRequest(db.Model):
    __tablename__ = 'serviceRequest'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    serviceId = db.Column(db.Integer, db.ForeignKey('Services.id'))
    customerId = db.Column(db.Integer, db.ForeignKey('Customer.id'))
    professionalId = db.Column(db.Integer, db.ForeignKey('Professional.id'))
    requestDate= db.Column(db.Date, nullable=False)
    completionDate= db.Column(db.Date)
    customerStatus = db.Column(db.String, default='requested')
    professionalStatus = db.Column(db.String, default='pending')
    reviewed = db.Column(db.String, default='no')
    
    service = db.relationship('Services', backref='serviceRequest', lazy=True)

class ServiceReview(db.Model):
    __tablename__ = 'ServiceReview'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    ServiceRequestId = db.Column(db.Integer, db.ForeignKey('serviceRequest.id'))
    serviceId = db.Column(db.Integer, db.ForeignKey('Services.id'))
    customerId = db.Column(db.Integer, db.ForeignKey('Customer.id'))
    professionalId = db.Column(db.Integer, db.ForeignKey('Professional.id'))
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    
    customer = db.relationship('Customer', backref='serviceReview', lazy=True)
    professional = db.relationship('Professional', backref='serviceReview', lazy=True)