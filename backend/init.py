from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from db_config import DB_CONFIG
from marshmallow import Schema, fields


app = Flask(__name__)
CORS(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

class UserCourse(db.Model):
    email = db.Column(db.String(100), db.ForeignKey('user.email'), primary_key=True)
    name = db.Column(db.String(100), db.ForeignKey('course.name'), primary_key=True)
    grade = db.Column(db.Integer, primary_key = True)
    semester = db.Column(db.String(100), primary_key = True)
    user = db.relationship('User', backref=db.backref('user_course_entries', cascade='all, delete-orphan'))
    course = db.relationship('Course', backref=db.backref('course_user_entries', cascade='all, delete-orphan'))
    def __init__(self, email, name, semester, grade):
        self.email = email
        self.name = name
        self.semester = semester
        self.grade = grade
        
class UserCourseSchema(ma.Schema):
    class Meta:
        fields = ("email", "name", "semester", "grade")
        model = UserCourse

user_schema = UserCourseSchema()

class SemesterSchema(Schema):
    semester = fields.Str()

semester_schema = SemesterSchema(many=True)