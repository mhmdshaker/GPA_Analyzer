from flask import render_template, request, jsonify
from models.user import User, UserSchema
from models.course import Course, CourseSchema
import bcrypt
from init import app, db, ma
import jwt, datetime
from db_config import SECRET_KEY

if __name__ == "__main__":
    app.run(debug=True)

user_schema = UserSchema()
course_schema = CourseSchema()




#creates a token when logging in
def create_token(email):
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=4),
        "iat": datetime.datetime.utcnow(),
        "email": email,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

#gets the token of the logged in user from the session
def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get("Authorization")
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None

#gets the user's email from the token
def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, "HS256")
    return payload["email"]


#create a user:
@app.route('/users', methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    new_user = User(email, password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)
    
#sign in:
@app.route('/sign_in', methods=['GET'])
def sign_in():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.hashed_password, password):
        token = create_token(email)
        return user_schema.jsonify(user)
    else:
        return jsonify({'error': 'Invalid email or password'})
    
#list all courses:
@app.route('/courses_search', methods=['GET'])
def search_courses():
    course_name = request.args.get('name')
    courses = Course.query.filter(Course.name.contains(course_name)).all()
    return jsonify(course_schema.dump(courses, many=True))

# #add a grade to a course for a specific user:


    