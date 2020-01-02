import datetime
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .. import linebot, webhook, db
from ..models.users import User, UserStatus

def checkEvent(args):
    return args.message.text.startswith("verify")

def handleEvent(args):

    # get code
    code = args.message.text
    code = code[code.find(' ')+1:]

    # query user
    user = User.query.filter_by(verify_code = code).first()

    # nobody ?
    if not user:
        return TextSendMessage(text="Authentication failed")

    # test if the verification code is outdated and it is correct
    if datetime.datetime.now() > user.verify_due or user.verify_code != code:
        return TextSendMessage(text="Authentication failed")

    # update status
    user.userid = args.source.user_id
    user.status = UserStatus.regisited
    user.verify_code = None
    user.verify_due = None
    db.session.commit()

    # link rich menu for user
    user.linkRichMenu()

    return TextSendMessage(text="Successful!")
