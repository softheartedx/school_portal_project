from flask_app import app
from flask_app.models.classroom_model import Class
from flask import render_template, request, redirect, session, flash

@app.route('/all_classes')
def vieww_all_classes():
    return render_template('all_classes.html', all_classes=Class.get_all_classes())