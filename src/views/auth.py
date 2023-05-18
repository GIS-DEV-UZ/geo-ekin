from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user
from src.forms.user import RegistrationForm, LoginForm
from src.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


class Auth():

    def login():
        if current_user.is_authenticated:
            return redirect(url_for('base_route.home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                next_page = request.args.get('next')
                login_user(user)
                return redirect(next_page) if next_page else redirect(url_for('base_route.home'))
            else:
                pass

        return render_template('login.html', form=form)

    def register():

        if current_user.is_authenticated:
            return redirect(url_for('base_route.home'))

        form = RegistrationForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Siz oldin registratsiyadan o`tgansz, qayta urinib ko`ring', 'danger')
                return redirect(url_for('auth.register'))
            else :
                hashed_password = generate_password_hash(form.password.data).decode('utf-8')
                user = User(first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=hashed_password,
                            email=form.email.data)
                user.create()

                return redirect(url_for('auth.login'))

        return render_template('register.html', form=form)
