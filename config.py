import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    # Ensure SECRET_KEY is loaded from environment or defaults to a fallback
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key_here')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY not set. Please set it in your environment.")

    # Ensure DATABASE_URL is set or fallback to SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///royal_enfield.db')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL not set. Please set it in your environment.")

    # Disable modification tracking for performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Set Flask Debug Mode based on the environment variable
    DEBUG = os.environ.get('FLASK_DEBUG', True)

