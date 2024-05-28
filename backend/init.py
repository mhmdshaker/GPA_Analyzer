from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from db_config import DB_CONFIG

app = Flask(__name__)
CORS(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

user_courses = db.Table('user_courses',
    db.Column('email', db.String(100), db.ForeignKey('user.email'), primary_key=True),
    db.Column('name', db.String(100), db.ForeignKey('course.name'), primary_key=True),
    db.Column('semester', db.String(100)),
    db.Column('grade', db.Integer)
)