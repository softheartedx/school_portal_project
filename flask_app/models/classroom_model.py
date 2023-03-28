from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.enrollment_model import Enrollment
import pprint

db = 'student_portal'


class Class:
    def __init__(self, data):
        self.id = data['id']
        self.class_name = data['class_name']
        self.description = data['description']
        self.location = data['location']
        self.start_date = data['start_date']
        self.students = []
        self.teacher = None

    @classmethod
    def save(cls, data):
        query = 'INSERT into classes(class_name, description, location, start_date, teacher) VALUES(%(class_name)s, %(description)s, %(location)s, %(start_date)s, %(teacher)s)'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def edit_class(cls, data, id):
        query = f'UPDATE classes SET class_name = %(class_name)s, description = %(description)s, location = %(location)s, start_date = %(start_date)s, teacher = %(teacher)s WHERE id = {id}'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one_class(cls, class_id):
        query = 'SELECT * FROM classes WHERE id=%(class_id)s'
        result = connectToMySQL(db).query_db(query, class_id)
        print(result)
        return result


    @classmethod
    def get_all_classes(cls):
        query = 'SELECT * FROM classes'
        return connectToMySQL(db).query_db(query)
