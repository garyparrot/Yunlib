from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from .. import linebot, webhook
from ..linemodels.booklist import MyBooklistRender, config as renderConfig
from ..crawlers import MyBooks 
from ..models.users import User
from .. import db
from flask import current_app as app

def checkEvent(args):
    return args.message.text.startswith("查詢我借的書")

def handleEvent(args):

    # Query user info
    print(args)
    user = User.query.filter_by(userid = args.source.user_id).first()

    try:
        if user:
            mybooks = MyBooks.crawler(user.lib_username, user.lib_password)
            config = renderConfig(**{
                    "lfooter": f"共{len(mybooks)}本書",
                    "rfooter": f"處理時間: {datetime.datetime.now().strftime('%m/%d %H:%M')}",
                    "books": mybooks,
                    "title": f"{user.lib_username}的借書資料",
                    "emptyhint": "你沒有借任何書:("
            })
            render = MyBooklistRender(config).render()
            return FlexSendMessage(alt_text="My books", contents = render)
    except Exception as ex:
        app.logger.error(str(ex))
        return TextSendMessage(text = "Oops, something fucked up.")

    return TextSendMessage(text = "Cannot obtain your information")
