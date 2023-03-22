from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
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
    
    #NEED JOIN QUERIES

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
        # if len(user['current_grade']) <= 0:
        #     flash("Please enter your current grade.")
        #     is_valid = False
        if len(user['password']) <= 5:
            flash("Your password must be at least 8 characters long.")
            is_valid = False
        if not email_REGEX.match(user['email']):
            flash('Your email is invalid.')
            is_valid = False
        if not user['password'] == user['cpassword']:
            flash("Your password does not match.")
            is_valid = False
        return is_valid
