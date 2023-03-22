from flask_app import app
from flask import render_template, request, redirect, session, flash

@app.route('/all_classes')
def vieww_all_classes():
    return render_template('all_classes.html')