from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .. import linebot, webhook

def checkEvent(args):
    return args.message.text.startswith("查詢我借的書")

def handleEvent(args):
    return TextSendMessage(text="My Books")
