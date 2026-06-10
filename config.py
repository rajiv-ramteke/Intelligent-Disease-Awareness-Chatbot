import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-12345')
    NVIDIA_API_KEY = os.environ.get('NVIDIA_API_KEY')
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///database/healthbot.db')
