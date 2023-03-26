from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.enrollment_model import Enrollment
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('student_register.html')

@app.route('/success')
def success():
    if 'user_id' not in session:
        flash("You must log in to access this page!")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    one_student = User.show_student_with_classes(data)
    return render_template('student_dashboard.html', student=User.get_user_by_id(session['user_id']), one_student=one_student)

@app.route('/success/teacher')
def success_teacher():
    if 'user_id' not in session:
        flash("You must log in to access this page!")
        return redirect('/')
    return render_template('teacher_dashboard.html', teacher=User.get_user_by_id(session['user_id']))

@app.route('/register', methods=['post'])
def register():
    if not User.user_validator(request.form):
        return redirect ('/')
    if User.get_user_by_email(request.form)==True:
        flash('This email address is already in use!')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'current_grade': request.form['current_grade'],
        'role': request.form['role'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    print(request.form)
    return redirect('/success')

@app.route('/login', methods=['post'])
def login_route():
    data = {'email': request.form['email']}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("The email or password is incorrect!")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("The email or password is incorrect!")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/success')



@app.route('/teacher_registration')
def teacher_registration():
    return render_template('teacher_register.html')

@app.route('/register/teacher', methods=['post'])
def register_teacher():
    if not User.user_validator(request.form):
        return redirect ('/')
    if User.get_user_by_email(request.form)==True:
        flash('This email address is already in use!')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'current_grade': request.form['current_grade'],
        'role': request.form['role'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    print(request.form)
    return redirect('/success/teacher')

@app.route('/login_page')
def login():
    return render_template('login.html')


@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')


@app.route('/show_student_profile/<int:student_id>')
def edit_profile(student_id):
    return render_template('edit_profile.html', one_student=User.get_user_by_id(student_id))

@app.route('/edit_student_profile/<int:student_id>', methods=['POST'])
def update_profile(student_id):
    if not User.user_validator(request.form):
        return redirect(f'/show_student_profile/{student_id}')
    User.update_student(request.form, student_id)
    print(request.form)
    return redirect('/success')
