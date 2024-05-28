from init import db, ma, user_courses
import bcrypt

#To access all the courwses of a user, use the courses attribute
class User(db.Model):
    email = db.Column(db.String(30), unique = True, primary_key = True)
    hashed_password = db.Column(db.String(128))
    courses = db.relationship('Course', secondary = user_courses, backref = db.backref('users', lazy = True))
    def __init__(self, email, password):
        super(User, self).__init__()
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        fields = ("email", "courses")
        model = User

user_schema = UserSchema()