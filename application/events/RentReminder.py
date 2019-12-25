from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .. import linebot, webhook

def checkEvent(args):
    # The event won't active by user interaction
    return False

def handleEvent(args):
    return TextSendMessage(text="Query Books")
