from flask import render_template, request, jsonify
from models.user import User, UserSchema
from models.course import Course, CourseSchema
import bcrypt
from init import app, db, ma, UserCourse, UserCourseSchema, semester_schema
import jwt, datetime
from db_config import SECRET_KEY
from marshmallow import Schema, fields

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
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid email or password'})

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
    
    #search if any course in the db has the same semester in the db:
    course_semester = Course.query.filter_by(semester=semester).all()
    found = False
    for x in course_semester:
        if x.name == course_name:
            found = True
            break
    if not found:
        return jsonify({'message': 'Course not found in this semester'}), 404
    
    if not course or not user:
        return jsonify({'message': 'Course or user not found'}), 404
    # Create a new CourseUser instance
    course_user = UserCourse(name=course.name, email=user.email, grade=grade, semester=semester)
    # Add the new CourseUser to the database
    db.session.add(course_user)
    db.session.commit()

    return jsonify({'message': 'Grade added successfully'}), 200

#display GPA of User:
@app.route('/gpa', methods=['GET'])
def display_gpa():
    token = extract_auth_token(request)
    user_email = None
    if token:
        try:
            user_email = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired."}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token."}), 403

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_courses = UserCourse.query.filter_by(email=user_email).all()
    total_credits = 0
    total_grade_points = 0
    for x in user_courses:
        total_credits += x.course.credits
        total_grade_points += x.grade * x.course.credits
    if (total_credits == 0):
        return jsonify({'gpa': 0}), 200
    gpa = total_grade_points / total_credits
    return jsonify({'gpa': gpa}), 200

#list all semesters:
@app.route('/semesters_search', methods=['GET'])
def search_semesters():
    semester = request.args.get('name')
    courses = Course.query.filter(Course.semester.contains(semester)).all()
    semesters = [{"semester": course.semester} for course in courses]
    #remove duplicates:
    semesters = list(set([semester['semester'] for semester in semesters]))
    semesters = [{"semester": semester} for semester in semesters]
    semesters.sort(key=lambda semester: semester['semester'])
    return jsonify(semester_schema.dump(semesters, many=True))

#list all courses:
@app.route('/courses_search', methods=['GET'])
def search_courses():
    course_name = request.args.get('name')
    semester = request.args.get('semester')
    #keep the courses that have the semester name as an attribute
    courses = Course.query.filter_by(semester=semester).all()
    courses_in_semester = []
    for course in courses:
        if course.semester == semester:
            courses_in_semester.append(course)
    return jsonify(course_schema.dump(courses_in_semester, many=True))

#display all grades of a user, divided per semester:
@app.route('/grades', methods=['GET'])
def display_grades():
    token = extract_auth_token(request)
    user_email = None
    if token:
        try:
            user_email = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired."}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token."}), 403

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_courses = UserCourse.query.filter_by(email=user_email).all()
    semesters = []
    for x in user_courses:
        semesters.append(x.semester)
    semesters = list(set(semesters))
    semesters.sort()
    grades = []
    for semester in semesters:
        courses = UserCourse.query.filter_by(email=user_email, semester=semester).all()
        grades_per_semester = []
        for course in courses:
            grades_per_semester.append({"course": course.name, "grade": course.grade})
        grades.append({"semester": semester, "courses": grades_per_semester})

    return jsonify(grades)

#delete a grade:
@app.route('/delete_grade', methods=['POST'])
def delete_grade():
    course_name = request.json['course']
    semester = request.json['semester']
    token = extract_auth_token(request)
    user_email = None
    if token:
        try:
            user_email = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired."}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token."}), 403

    course = Course.query.filter_by(name=course_name).first()
    user = User.query.filter_by(email=user_email).first()
    if not course or not user:
        return jsonify({'message': 'Course or user not found'}), 404

    course_user = UserCourse.query.filter_by(name=course_name, email=user_email, semester=semester).first()
    if not course_user:
        return jsonify({'message': 'Grade not found'}), 404

    db.session.delete(course_user)
    db.session.commit()
    return jsonify({'message': 'Grade deleted successfully'}), 200