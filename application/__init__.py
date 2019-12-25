from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi, WebhookHandler

db = SQLAlchemy()

def create_app():

    app = Flask(__name__, instance_relative_config = False, static_folder = None)

    # Configuration
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)


    # Configuration for linebot API.
    # Trust me, This is necessary evil.
    global linebot 
    global webhook
    linebot = LineBotApi(app.config['LINEBOT_ACCESS_TOKEN'])
    webhook = WebhookHandler(app.config['LINEBOT_SECRET'])

    with app.app_context():

        # Create tables for our models
        db.create_all()

        # trigger request_handler
        from . import request_handler

        # blueprints
        from .routes import auth
        app.register_blueprint(auth.blueprint)

        return app
