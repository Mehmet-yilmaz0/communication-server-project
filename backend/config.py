import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/communication_db')
    JWT_SECRET = os.getenv('JWT_SECRET', 'change-this-secret-key-in-production')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = ['http://localhost:3000']

