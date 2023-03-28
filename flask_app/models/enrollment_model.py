from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL


db = 'student_portal'

class Enrollment:
    def __init__(self, data):
        self.student_id = data['student_id']
        self.class_id = data['class_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.student = None

    @classmethod
    def enroll_in_class(cls, data):
        query = 'INSERT INTO enrollment (student_id, class_id) VALUES(%(student_id)s, %(class_id)s)'
        return connectToMySQL(db).query_db(query, data)
    

    