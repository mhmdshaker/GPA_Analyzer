from init import db, ma, UserCourse
import bcrypt
from marshmallow import fields


#To access all the courwses of a user, use the courses attribute
from sqlalchemy.ext.associationproxy import association_proxy

class User(db.Model):
    email = db.Column(db.String(30), unique=True, primary_key=True)
    hashed_password = db.Column(db.String(128))
    user_courses = db.relationship('UserCourse', backref='user_entry')
    courses = association_proxy('user_courses', 'course')

    def __init__(self, email, password):
        super(User, self).__init__()
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        fields = ("email", "courses")
        model = User
    courses = fields.Nested('CourseSchema', many=True)

user_schema = UserSchema()