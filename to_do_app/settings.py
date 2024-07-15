import os

FLASK_ENV = os.getenv("FLASK_ENV", "production")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///todos.db")
SECRET_KEY = os.getenv("APP_SECRET_KEY")
