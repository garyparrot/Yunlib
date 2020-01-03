from linebot.models import MessageEvent, TextMessage, TextSendMessage
from ..models.users import User
from .. import linebot, webhook

def checkEvent(args):
    return args.message.text.startswith("使用者資訊")

def handleEvent(args):
    user = User.query.filter_by(userid = args.source.user_id).first()

    if user:
        return TextSendMessage(text = "Hi, %s" % user.lib_username)
    else:
        return TextSendMessage(text = "你還沒有註冊")

