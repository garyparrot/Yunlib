from .. import db
from .. import linebot
from flask import current_app as app

class UserStatus:
    requireVerify = "requireVerify"
    regisited     = "regisited"

class User(db.Model):
    userid       = db.Column(db.String(32), unique=True,  nullable=False, primary_key=True)
    lib_username = db.Column(db.String(64), unique=False, nullable=False)
    lib_password = db.Column(db.String(64), unique=False, nullable=False)
    status       = db.Column(db.String(32), unique=False, nullable=False, default = UserStatus.requireVerify)
    verify_code  = db.Column(db.String(16), unique=True,  nullable=True)
    verify_due   = db.Column(db.DateTime,   unique=False, nullable=True)

    def linkRichMenu(self, target = "RichMenu"):
        menus = linebot.get_rich_menu_list()
        menu  = [ menu for menu in menus if menu.name == target ][0]
        linebot.link_rich_menu_to_user(self.userid, menu.rich_menu_id)

    def __repr__(self):
        return f"<User ${self.userid}>"

