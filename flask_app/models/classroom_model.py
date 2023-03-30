from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.enrollment_model import Enrollment
from flask_app.models import user_model
import pprint

db = 'student_portal'


class Class:
    def __init__(self, data):
        self.id = data['id']
        self.class_name = data['class_name']
        self.location = data['location']
        self.start_date = data['start_date']
        self.description = data['description']
        self.students = []
        self.teacher = None

    @classmethod
    def save(cls, data):
        query = 'INSERT into classes(class_name, description, location, start_date, teacher_id) VALUES(%(class_name)s, %(description)s, %(location)s, %(start_date)s, %(teacher_id)s)'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def edit_class(cls, data, id):
        query = f'UPDATE classes SET class_name = %(class_name)s, description = %(description)s, location = %(location)s, start_date = %(start_date)s, teacher_id = %(teacher_id)s WHERE id = {id}'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_class(cls, data):
        query = 'SELECT * FROM classes JOIN users on classes.teacher_id = users.id WHERE classes.id = %(class_id)s'
        results = connectToMySQL(db).query_db(query, data)
        one_class = cls(results[0])
        for items in results[0]:
            print(items)
        for row_in_db in results:
            teacher_data = {
                'id': row_in_db['users.id'],
                "first_name":  row_in_db['first_name'],
                "last_name": row_in_db['last_name'],
                "current_grade": row_in_db['current_grade'],
                "role": row_in_db['role'],
                'email': row_in_db['email'],
                'password': row_in_db['password'],
            }
            one_class.teacher = user_model.User(teacher_data)
        return one_class

    @classmethod
    def get_all_classes(cls):
        query = 'SELECT * FROM classes'
        return connectToMySQL(db).query_db(query)
    
    @classmethod
    def delete_class(cls, data):
        query = 'DELETE FROM classes WHERE id=%(id)s'
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def class_validator(class_data):
        is_valid = True
        if len(class_data['class_name']) <= 0 or len(class_data['location']) <= 0 or len(class_data['start_date']) <= 0 or len(class_data['description']) <= 0:
            flash('All fields are required!')
            is_valid = False
        if len(class_data['class_name']) <= 1:
            flash("The class name must be at least 2 characters long.")
            is_valid = False
        if len(class_data['location']) <= 2:
            flash("The location must be at least 2 characters long.")
            is_valid = False
        if len(class_data['start_date']) < 1:
            flash("Select a start date.")
            is_valid = False
        if len(class_data['description']) <= 2:
            flash("The class description is too short.")
            is_valid = False
        return is_valid

    @staticmethod
    def class_validator(class_data):
        is_valid = True
        if len(class_data['class_name']) <= 0 or len(class_data['location']) <= 0 or len(class_data['start_date']) <= 0 or len(class_data['description']) <= 0:
            flash('All fields are required!')
            is_valid = False
        if len(class_data['class_name']) <= 2:
            flash("The class name must be at least 2 characters long.")
            is_valid = False
        if len(class_data['location']) <= 2:
            flash("The location must be at least 2 characters long.")
            is_valid = False
        if len(class_data['start_date']) < 1:
            flash("Select a start date.")
            is_valid = False
        if len(class_data['description']) <= 2:
            flash("The class description is too short.")
            is_valid = False
        return is_valid