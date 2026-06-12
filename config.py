import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'healthbot-pro-secret-2024-xyz')
    NVIDIA_API_KEY = os.environ.get('NVIDIA_API_KEY')
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///database/healthbot.db')
    
    # Session settings for production (Hugging Face iframe requires SameSite=None and Secure=True)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'None'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
