from flask_app import app
from flask_app.models.classroom_model import Class
from flask_app.models.user_model import User
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
    return render_template('student_view_class.html', class_info = one_class, teacher_classes=User.teacher_with_classes({'id': session['user_id']}))

@app.route('/delete_class/<int:id>')
def delete_class(id):
    data = {
        'id': id
    }
    Class.delete_class(data)
    return redirect('/success')


#NOT USING THIS YET
@app.route('/show_one_class/<int:class_id>')
def get_one_class_teacher(class_id):
    data = {
        'class_id': class_id
    }
    one_class = User.show_student_with_classes(data)
    return render_template('teacher_view_class.html', class_info = one_class)

@app.route('/save_class/<int:teacher_id>', methods=['POST'])
def save_class(teacher_id):
    if not Class.class_validator(request.form):
        return redirect('/success')
    data = {
        'class_name': request.form['class_name'],
        'location': request.form['location'],
        'start_date': request.form['start_date'],
        'description': request.form['description'],
        'teacher_id': teacher_id
    }
    print(data)
    Class.save(data)
    return redirect('/success')


