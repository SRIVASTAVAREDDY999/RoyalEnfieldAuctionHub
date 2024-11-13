import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key_here')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///royal_enfield.db')  # Database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance
