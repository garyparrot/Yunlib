from flask import current_app as app
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from ...models.users import User
from ... import db

def checkEvent(args):
    return args.message.text.startswith("新增使用者") or args.message.text.startswith("adduser")

def failure(args, message):
    return TextSendMessage(text="[Failure]\n" + message)

def handleEvent(args):
    cmd = args.message.text.split(' ')

    if len(cmd) != 4: return failure(args, "Argument size not match.")

    app.logger.info("Debug adduser: %s %s %s", cmd[1], cmd[2], cmd[3])

    newuser = User(
        userid       = cmd[1],
        lib_username = cmd[2],
        lib_password = cmd[3]
    )
    db.session.add(newuser)
    db.session.commit()

    return TextSendMessage(text="Done")
