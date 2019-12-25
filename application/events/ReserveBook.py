from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .. import linebot, webhook

def checkEvent(args):
    return args.message.text.startswith("預約")

def handleEvent(args):
    return TextSendMessage(text="Reserve Books")
