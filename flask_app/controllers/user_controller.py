from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.classroom_model import Class
from flask_app.models.enrollment_model import Enrollment
from flask_app.models.classroom_model import Class

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


#LOGIN/REGISTER ROUTES
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/student_registration_page')
def student_reg():
    return render_template('student_register.html')

@app.route('/teacher_registration_page')
def teacher_reg():
    return render_template('teacher_register.html')

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')



@app.route('/register/<role>', methods=['post'])
def register(role):
    temp_dict = dict(request.form)
    print(request.form)
    if role == 'teacher':
        temp_dict['current_grade'] = '1'
    if role == 'student':
        temp_dict['role'] = 'student'
    if not User.user_validator(temp_dict):
        if role == 'teacher':
            return redirect('/teacher_registration_page')
        if role == 'student':
            return redirect('/student_registration_page')
    if User.get_user_by_email(request.form) != False:
        flash('This email address is already in use!')
        if role == 'teacher':
            return redirect('/teacher_registration_page')
        if role == 'student':
            return redirect('/student_registration_page')
    print(temp_dict)
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': temp_dict['first_name'],
        'last_name': temp_dict['last_name'],
        'current_grade': temp_dict['current_grade'],
        'role': temp_dict['role'],
        'email': temp_dict['email'],
        'password': pw_hash
    }
    print(data)
    user_id = User.save(data)
    session['user_id'] = user_id
    print(request.form)
    return redirect('/success')


@app.route('/login', methods=['post'])
def login_route():
    data = {'email': request.form['email']}
    user_in_db = User.get_user_by_email(data)
    print(user_in_db)
    if not user_in_db:
        flash("The email or password is incorrect!")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("The email or password is incorrect!")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/success')


@app.route('/success')
def success():
    if 'user_id' not in session:
        flash("You must log in to access this page!")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    one_student = User.show_student_with_classes(data)
    all_classes = Class.get_all_classes()
    print(one_student)
    if one_student.role != 'student':
        return render_template('teacher_dashboard.html', user=User.get_user_by_id(session['user_id']), one_student=one_student, all_classes=Class.get_all_classes(), teacher_classes=User.teacher_with_classes(data))
    if one_student.role == 'student':
        return render_template('student_dashboard.html', user=User.get_user_by_id(session['user_id']), one_student=one_student)


#EDIT USER PROFILE ROUTES
@app.route('/show_student_profile/<int:student_id>')
def edit_profile(student_id):
    return render_template('edit_profile.html', one_student=User.get_user_by_id(student_id))


@app.route('/edit_student_profile/<int:student_id>', methods=['POST'])
def update_profile1(student_id):
    if not User.update_user_validator(request.form):
        return redirect(f'/show_student_profile/{student_id}')
    User.update_student(request.form, student_id)
    print(request.form)
    return redirect('/success')

@app.route('/edit_student_profile/<int:student_id>', methods=['POST'])
def update_profile(student_id):
    if not User.update_user_validator(request.form):
        return redirect('/success')
    User.update_student(request.form, student_id)
    print(request.form)
    return redirect('/success')
