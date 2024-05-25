from flask import Flask, render_template, request, jsonify
from init import app, db, ma
from models.user import User, UserSchema
from models.course import Course, CourseSchema
import bcrypt

user_schema = UserSchema()
course_schema = CourseSchema()

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
        return user_schema.jsonify(user)
    else:
        return jsonify({'error': 'Invalid email or password'})
    
#list all courses:
@app.route('/courses_search', methods=['GET'])
def search_courses():
    course_name = request.args.get('name')
    courses = Course.query.filter(Course.name.contains(course_name)).all()
    return jsonify(course_schema.dump(courses, many=True))

#add a grade to a course for a specific user: