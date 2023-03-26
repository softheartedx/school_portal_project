from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.enrollment_model import Enrollment
from flask_bcrypt import Bcrypt


@app.route('/enroll_in_class/<int:class_id>', methods=['post'])
def enroll_in_class(class_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'student_id': session['user_id'],
        'class_id': class_id
    }
    Enrollment.enroll_in_class(data)
    return redirect('/success')
