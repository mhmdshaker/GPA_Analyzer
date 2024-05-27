from init import db, ma
import bcrypt

class User(db.Model):
    email = db.Column(db.String(30), unique = True, primary_key = True)
    hashed_password = db.Column(db.String(128))
    def __init__(self, email, password):
        super(User, self).__init__()
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        fields = ("email",)
        model = User

user_schema = UserSchema()