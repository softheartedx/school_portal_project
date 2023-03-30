from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.classroom_model import Class
from flask_app.models.enrollment_model import Enrollment
import pprint
import re

email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'student_portal'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.current_grade = data['current_grade']
        self.role = data['role']
        self.email = data['email']
        self.password = data['password']
        self.classes = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users(first_name, last_name, current_grade, role, email, password) VALUES(%(first_name)s, %(last_name)s, %(current_grade)s, %(role)s, %(email)s, %(password)s)'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(db).query_db(query, data)
        if len(result) == 0:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, id):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        result = connectToMySQL(db).query_db(query, {'id': id})
        return cls(result[0])

    @classmethod
    def update_student(cls, data, id):
        query = f'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, current_grade=%(current_grade)s, role=%(role)s, email=%(email)s WHERE id={id}'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def show_student_with_classes(cls, id):
        query = '''SELECT * FROM users
                LEFT JOIN enrollment on enrollment.student_id = users.id
                LEFT JOIN classes on enrollment.class_id = classes.id WHERE users.id =%(id)s'''
        results = connectToMySQL(db).query_db(query, id)
        one_student = cls(results[0])
        for row_in_db in results:
            enrollment_data = {
                'student_id': row_in_db['student_id'],
                'class_id': row_in_db['class_id'],
                'created_at': row_in_db['enrollment.created_at'],
                'updated_at': row_in_db['enrollment.updated_at'],
            }
            one_class_data = {
                'id': row_in_db['classes.id'],
                "class_name":  row_in_db['class_name'],
                "description": row_in_db['description'],
                "location": row_in_db['location'],
                "start_date": row_in_db['start_date'],
                'created_at': row_in_db['classes.created_at'],
            }
            one_student.classes.append(Class(one_class_data))
        return one_student

    @classmethod
    def teacher_with_classes(cls, id):
        query = 'SELECT * FROM users JOIN classes on classes.teacher_id = %(id)s'
        results = connectToMySQL(db).query_db(query, id)
        one_teacher = cls(results[0])
        for row_in_db in results:
            one_class_data = {
                'id': row_in_db['classes.id'],
                "class_name":  row_in_db['class_name'],
                "description": row_in_db['description'],
                "location": row_in_db['location'],
                "start_date": row_in_db['start_date'],
                'created_at': row_in_db['classes.created_at'],
            }
            one_teacher.classes.append(Class(one_class_data))
        return one_teacher

    @staticmethod
    def user_validator(user):
        is_valid = True
        if len(user['first_name']) <= 0 or len(user['last_name']) <= 0 or len(user['current_grade']) <= 0 or len(user['email']) <= 0 or len(user['password']) <= 0:
            flash('All fields are required!')
            is_valid = False
        if len(user['first_name']) <= 2:
            flash("Your first name must be at least 2 characters long.")
            is_valid = False
        if len(user['last_name']) <= 2:
            flash("Your last name must be at least 2 characters long.")
            is_valid = False
        if len(user['current_grade']) < 1:
            flash("Your grade must be at least 1 characters long.")
            is_valid = False
        if len(user['role']) <= 2:
            flash("Your role must be at least 2 characters long.")
            is_valid = False
        if not email_REGEX.match(user['email']):
            flash('Your email is invalid.')
            is_valid = False
        if len(user['password']) <= 5:
            flash("Your password must be at least 8 characters long.")
            is_valid = False
        if not user['password'] == user['cpassword']:
            flash("Your password does not match.")
            is_valid = False
        return is_valid

    @staticmethod
    def update_user_validator(user):
        is_valid = True
        if len(user['first_name']) <= 0 or len(user['last_name']) <= 0 or len(user['current_grade']) <= 0 or len(user['role']) <= 0 or len(user['email']) <= 0:
            flash('All fields are required!')
            is_valid = False
        if len(user['first_name']) <= 2:
            flash("Your first name must be at least 2 characters long.")
            is_valid = False
        if len(user['last_name']) <= 2:
            flash("Your last name must be at least 2 characters long.")
            is_valid = False
        if len(user['current_grade']) < 1:
            flash("Your grade must be at least 1 characters long.")
            is_valid = False
        if len(user['role']) <= 2:
            flash("Your role must be at least 2 characters long.")
            is_valid = False
        if not email_REGEX.match(user['email']):
            flash('Your email is invalid.')
            is_valid = False
        return is_valid
