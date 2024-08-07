from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()
gravatar = Gravatar(size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    Bootstrap5(app)
    gravatar.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Set the login view and message
    login_manager.login_view = 'auth.register'
    login_manager.login_message = 'Please log in to access this page.'

    with app.app_context():
        from .routes import auth, main, blog
        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)
        app.register_blueprint(blog.bp)

    return app