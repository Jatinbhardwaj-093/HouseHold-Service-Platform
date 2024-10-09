from flask import Flask,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
import config
db = SQLAlchemy(app)

import models

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Change port and host
