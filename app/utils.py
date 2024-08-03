from functools import wraps
from flask import abort
from flask_login import current_user
import yagmail

from . import db
from .models import Comment
from .config import Config

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
        comment = Comment.query.filter_by(author_id=current_user.id).first()
        if not current_user.is_authenticated or (comment and current_user.id != comment.author_id):
            return abort(403)
        return function(*args, **kwargs)
    return check

def send_email(name, email, phone, message):
    email_message = f"\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    try:
        yag = yagmail.SMTP(user=Config.MAIL_ADDRESS, password=Config.MAIL_PASSWORD)
        yag.send(to=Config.MAIL_ADDRESS, subject="New Message from BLOG-POST contact", contents=email_message)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        # You might want to log this error or handle it in some way
