from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
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
    return render_template('student_dashboard.html', student=User.get_user_by_id(session['user_id']))

@app.route('/register', methods=['post'])
def register():
    if not User.user_validator(request.form):
        return redirect ('/')
    # if User.get_user_by_email(request.form)==True:
    #     flash('This email address is already in use!')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'current_grade': request.form['current_grade'],
        'role': request.form['role'],
        'email': request.form['email'],
        'password': request.form['password']
    }
    user_id = User.save(data)
    session['first_name'] = request.form['first_name']
    session['user_id'] = user_id
    print(request.form)
    return redirect('/success')

# @app.route LOGIN HERE

@app.route('/teacher_registration')
def teacher_registration():
    return render_template('teacher_register.html')

@app.route('/login_page')
def login():
    return render_template('login.html')


@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')


@app.route('/edit_profile/<int:id>')
def edit_profile(id):
    return render_template('edit_profile.html', one_student=User.get_user_by_id(id))

