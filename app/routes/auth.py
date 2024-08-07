from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User
from app.forms import RegisterForm, LoginForm

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        existing_email = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()
        
        if existing_email:
            flash("Email address already registered", "error")
            return redirect(url_for("auth.login"))
        elif existing_username:
            flash("Username already registered", "error")
            return redirect(url_for("auth.register"))
        else:
            register_user = User(
                password=generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=24),
                username=form.username.data,
                email=form.email.data
            )
            db.session.add(register_user)
            db.session.commit()
            login_user(register_user)
            return redirect(url_for("main.get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)

@bp.route('/login', methods=["GET", "POST"])
def login():
    user_form = LoginForm()
    if user_form.validate_on_submit():
        email = user_form.email.data
        password = user_form.password.data
        user_data = User.query.filter_by(email=email).first()
        if not user_data:
            flash("That email does not exist, please try again.")
            return redirect(url_for("auth.login"))
        elif not check_password_hash(user_data.password, password):
            flash("Invalid Password. Please try again")
            return redirect(url_for("auth.login"))
        else:
            login_user(user_data)
            return redirect(url_for("main.get_all_posts"))
    return render_template("login.html", form=user_form, current_user=current_user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.get_all_posts'))
