from linebot.models import MessageEvent, TextMessage, TextSendMessage
from . import linebot, webhook
from .events import eventlist as events

@webhook.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.reply_token == "00000000000000000000000000000000":
        return

    for e in events:
        if e.checkEvent(event):
            response = e.handleEvent(event)
            linebot.reply_message(event.reply_token, response)
            return 

    linebot.reply_message(event.reply_token, TextSendMessage(text="Sorry, I don't understand your request."))

    return 
