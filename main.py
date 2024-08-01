from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import CreatePostForm, CommentForm, LoginForm, RegisterForm
import os
import yagmail

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

MAIL_ADDRESS = os.environ.get("EMAIL_KEY")
MAIL_PASSWORD = os.environ.get("PASSWORD_KEY")


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


def only_commenter(function):
    @wraps(function)
    def check(*args, **kwargs):
        user = db.session.execute(db.select(Comment).where(Comment.author_id == current_user.id)).scalar()
        if not current_user.is_authenticated or current_user.id != user.author_id:
            return abort(403)
        return function(*args, **kwargs)

    return check


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE TABLES

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


# TODO: Create a User table for all your registered users.
class User(UserMixin, db.Model):
    __tablename__ = "user_reg_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True)
    email: Mapped[str] = mapped_column(String(250), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    posts = relationship("BlogPost", back_populates="author")
    comment = relationship("Comment", back_populates="author")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("user_reg_info.id"))
    author = relationship("User", back_populates="comment")
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    post = relationship("BlogPost", back_populates="comment")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("user_reg_info.id"))
    author = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    # author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comment = relationship("Comment", back_populates="post")


with app.app_context():
    db.create_all()


# TODO: Use Werkzeug to hash the user's password when creating a new user.
# This contains all the codes required with the registration html and API
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    email = form.email.data
    username = form.username.data
    existing_email = User.query.filter_by(email=email).first()
    existing_username = User.query.filter_by(username=username).first()
    if form.validate_on_submit():
        if existing_email:
            flash("Email address already registered", "error")
            return redirect(url_for("login"))
        elif existing_username:
            flash("Username already registered", "error")
            return redirect(url_for("register"))
        else:
            register_user = User(
                password=generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=24),
                username=form.username.data,
                email=form.email.data
            )
            db.session.add(register_user)
            db.session.commit()
            login_user(register_user)
            return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login', methods=["GET", "POST"])
def login():
    user_form = LoginForm()
    if user_form.validate_on_submit():
        email = user_form.email.data
        password = user_form.password.data
        user_data = User.query.filter_by(email=email).first()
        if not user_data:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user_data.password, password):
            flash("Invalid Password.Please try again")
            return redirect(url_for("login"))
        else:
            login_user(user_data)
            return redirect(url_for("get_all_posts"))

    return render_template("login.html", form=user_form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    year = date.today().year
    return render_template("index.html", all_posts=posts, current_user=current_user, year=year)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            author=current_user,
            post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post.html", post=requested_post, current_user=current_user, form=form)
    # else:
    #     return render_template("post.html", post=requested_post, current_user=current_user)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, current_user=current_user)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/delete/comment/<int:comment_id>/<int:post_id>")
@only_commenter
def delete_comment(post_id, comment_id):
    post_to_delete = db.get_or_404(Comment, comment_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('show_post', post_id=post_id))


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        contact_form = request.form
        send_email(contact_form["name"], contact_form["email"], contact_form["phone"], contact_form["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    yag = yagmail.SMTP(user=MAIL_ADDRESS, password=MAIL_PASSWORD)
    yag.send(to=MAIL_ADDRESS, subject="New Message from BLOG-POST contact", contents=email_message)


if __name__ == "__main__":
    app.run(debug=False, port=5002)
