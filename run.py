from app import create_app, db
from app.config import Config
from flask_migrate import upgrade

app = create_app(Config)

@app.cli.command("db_upgrade")
def db_upgrade():
    """Run database migrations."""
    with app.app_context():
        upgrade()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)