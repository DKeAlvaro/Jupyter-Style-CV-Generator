import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')