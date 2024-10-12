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
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String, nullable=False)
    username= db.Column(db.String, nullable=False)
    password= db.Column(db.String, nullable=False)
    # I have a pseudo column name "serviceType" to fetch service details
    serviceId = db.Column(db.Integer, db.ForeignKey('Services.id'))
    experience= db.Column(db.Integer, nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    flag = db.Column(db.String, default='no')
    

class Services(db.Model):
    __tablename__ = 'Services'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    serviceName= db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.String)
    professionalServiceType = db.relationship('Professional', backref='serviceType', lazy=True)
    
    
# class Img(db.Model):
#     __tablename__ = 'Img'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text, nullable=False)
#     filepath = db.Column(db.String(200), nullable=False)
#     mimetype = db.Column(db.Text, nullable=False)
#     influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'))  
    
class ServiceRequest(db.Model):
    __tablename__ = 'serviceRequest'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    serviceId = db.Column(db.Integer, db.ForeignKey('Services.id'))
    customerId = db.Column(db.Integer, db.ForeignKey('Customer.id'))
    professionalId = db.Column(db.Integer, db.ForeignKey('Professional.id'))
    customerStatus = db.Column(db.String, default='requested')
    professionalStatus = db.Column(db.String, default='requested')
    service = db.relationship('Services', backref='serviceRequest', lazy=True)
    
