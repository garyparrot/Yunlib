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
        from .models import users
        db.create_all()

        # trigger request_handler
        from . import request_handler

        # scheduler
        from . import scheduler
        scheduler.startScheduler()

        # blueprints
        from .routes import auth
        from .routes import signup
        app.register_blueprint(auth.blueprint)
        app.register_blueprint(signup.blueprint)

        return app
