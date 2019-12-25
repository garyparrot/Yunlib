from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .. import linebot, webhook

def checkEvent(args):
    return args.message.text.startswith("搜尋")

def handleEvent(args):
    return TextSendMessage(text="Rent Reminder")
