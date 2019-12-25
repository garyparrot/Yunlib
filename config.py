import os

class Config:
    TEMPLATES_AUTO_RELOAD = os.environ.get("TEMPLATES_AUTO_RELOAD").lower() == "true"
    DEBUG = os.environ.get('DEBUG').lower() == "true"
    TESTING = os.environ.get('TESTING').lower() == "true"

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    LINEBOT_ACCESS_TOKEN = os.environ.get('linebot_access_token')
    LINEBOT_SECRET = os.environ.get('linebot_secret')
