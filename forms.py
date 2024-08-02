from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Length, ValidationError
from flask_ckeditor import CKEditorField
from email_validator import validate_email, EmailNotValidError


def validate_email_address(field):
    try:
        validate_email(field.data)
    except EmailNotValidError:
        raise ValidationError('Invalid email address.')


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired(), Length(5, message="Your Username should be a min of "
                                                                                 "5 character ")])
    email = StringField('Email', validators=[DataRequired(), validate_email_address])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(8, message="Your Username should be a min of "
                                                                           "5 character ")])
    submit = SubmitField("Submit")


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), validate_email_address])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(8, message="Your Username should be a min of "
                                                                           "5 character ")])
    submit = SubmitField("Login")


# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment = CKEditorField("Comment Below", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
