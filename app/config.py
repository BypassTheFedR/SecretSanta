import os
from dotenv import load_dotenv

# Specify the path to the .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    APP_PASSWORD = os.environ.get('APP_PASSWORD')

class Debug_Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    APP_PASSWORD = os.environ.get('APP_PASSWORD')

# Start debugging server as follows
# python -m aiosmtpd -n -l localhost:1025

