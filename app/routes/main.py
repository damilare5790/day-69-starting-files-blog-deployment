from flask import Blueprint, render_template, request
from flask_login import current_user
from datetime import date

from ..models import BlogPost
from ..utils import send_email

bp = Blueprint('main', __name__)

@bp.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    year = date.today().year
    return render_template("index.html", all_posts=posts, current_user=current_user, year=year)

@bp.route("/about")
def about():
    return render_template("about.html", current_user=current_user)

@bp.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        contact_form = request.form
        send_email(contact_form["name"], contact_form["email"], contact_form["phone"], contact_form["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)
