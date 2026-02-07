import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'postgresql')
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'hr_helpdesk')
    DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
    
    # Build database URI based on type
    if DATABASE_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_NAME}.db"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@"
            f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings
    CORS_HEADERS = 'Content-Type'
