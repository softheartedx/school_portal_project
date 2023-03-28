from flask_app import app
from flask_app.models.classroom_model import Class
from flask import render_template, request, redirect, session, flash


@app.route('/all_classes')
def view_all_classes():
    return render_template('join_class.html', all_classes=Class.get_all_classes())


@app.route('/show_one_class/<int:class_id>')
def get_one_class(class_id):
    data = {
        'class_id': class_id
    }
    one_class = Class.get_one_class(data)
    return render_template('student_view_class.html', class_info = one_class)

@app.route('/show_one_class/<int:class_id>')
def get_one_class_teacher(class_id):
    data = {
        'class_id': class_id
    }
    one_class = Class.get_one_class(data)
    return render_template('student_view_class.html', class_info = one_class)
