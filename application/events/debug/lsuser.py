from flask import current_app as app
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from ...models.users import User
from ... import db

def checkEvent(args):
    return args.message.text == "列出使用者" or args.message.text == "lsuser"

def handleEvent(args):
    cmd = args.message.text

    app.logger.info("Debug lsuser")

    userinfo = [ user.__repr__() for user in User.query.all()]
    userinfo = '\n'.join(userinfo) if len(userinfo) != 0 else "No user found."

    return TextSendMessage(text = userinfo)
