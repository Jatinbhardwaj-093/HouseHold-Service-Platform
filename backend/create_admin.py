from app import create_app
from models import Admin, db
from api import bcrypt

# Admin credentials
adminName = 'admin'
password = 'admin'

app = create_app()


with app.app_context():
    existing_admin = Admin.query.filter_by(username=adminName).first()
    if existing_admin:
        print(f"Admin user '{adminName}' already exists.")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = Admin(username=adminName, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{adminName}' created successfully.")