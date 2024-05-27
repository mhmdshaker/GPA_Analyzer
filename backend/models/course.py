from init import db, ma
import bcrypt

#to access all the users of a course, use the users attribute (not shown)
class Course(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    def __init__(self, name):
        self.name = name

class CourseSchema(ma.Schema):
    class Meta:
        fields = ("name", "users")
        model = Course

course_schema = CourseSchema()