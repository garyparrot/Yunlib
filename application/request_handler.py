from linebot.models import MessageEvent, TextMessage, TextSendMessage
from . import linebot, webhook

@webhook.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return
    linebot.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
