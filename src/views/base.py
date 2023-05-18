from flask import render_template

def home_controller():
    return render_template('index.html')

