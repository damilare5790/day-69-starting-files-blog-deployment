import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
    MAIL_ADDRESS = os.environ.get("EMAIL_KEY")
    MAIL_PASSWORD = os.environ.get("PASSWORD_KEY")
