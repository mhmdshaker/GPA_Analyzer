from flask import render_template, request, jsonify
from models.user import User, UserSchema
from models.course import Course, CourseSchema
import bcrypt
from init import app, db, ma, UserCourse, UserCourseSchema
import jwt, datetime
from db_config import SECRET_KEY

if __name__ == "__main__":
    app.run(debug=True)

user_schema = UserSchema()
course_schema = CourseSchema()
user_courses_schema = UserCourseSchema()


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
@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        token = create_token(email)
        print("succersss")
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid email or password'})
    
#list all courses:
@app.route('/courses_search', methods=['GET'])
def search_courses():
    course_name = request.args.get('name')
    courses = Course.query.filter(Course.name.contains(course_name)).all()
    return jsonify(course_schema.dump(courses, many=True))

# #add a grade to a course for a specific user:
@app.route('/add_grade', methods = ['POST'])
def add_grade():
    course_name = request.json['course']
    grade = request.json['grade']
    semester = request.json['semester']
    #to get the token from the session and get the email:
    token = extract_auth_token(request)
    user_email = None
    if token:
        try:
            #to get the email from the token
            user_email = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired."}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token."}), 403
    
    # Get the course and user from the database
    course = Course.query.filter_by(name=course_name).first()
    user = User.query.filter_by(email=user_email).first()
    if not course or not user:
        return jsonify({'message': 'Course or user not found'}), 404

    # Create a new CourseUser instance
    course_user = UserCourse(name=course.name, email=user.email, grade=grade, semester=semester)
    # Add the new CourseUser to the database
    db.session.add(course_user)
    db.session.commit()

    return jsonify({'message': 'Grade added successfully'}), 200
        
    
    