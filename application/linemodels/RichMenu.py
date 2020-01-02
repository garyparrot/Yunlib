import os
from linebot.models import *
from flask import current_app as app

def menuConfig():
    return {
        "size" : RichMenuSize(2500, 843),
        "name" : "RichMenu",
        "chat_bar_text" : "Yunlib chatbot",
        "areas" : [
            RichMenuArea( RichMenuBounds(  97, 0, 702, 843), PostbackAction(label="查詢我借的書", text="查詢我借的書", data="{'data': '查詢我借的書'}")),
            RichMenuArea( RichMenuBounds( 921, 0, 702, 843), PostbackAction(label="搜尋書目", text="搜尋書目", data="{'data': '搜尋書目'}")),
            RichMenuArea( RichMenuBounds(1740, 0, 702, 843), PostbackAction(label="使用者資訊", text="使用者資訊", data="{'data': '使用者資訊'}")),
            ],
        "selected" : False
    }

def initMenu(linebot):
    
    # Remove old menus
    for menu in linebot.get_rich_menu_list():
        linebot.delete_rich_menu(menu.rich_menu_id)

    # Create Menu
    menu = RichMenu(**menuConfig())

    # Create Menu
    menu_id = linebot.create_rich_menu(menu)

    # Upload Menu image file
    menu_image = os.path.join(app.root_path, "linemodels", "RichMenu", "rich_menu.png")
    with open(menu_image, "rb") as image:
        linebot.set_rich_menu_image(menu_id, "image/png", image)

    app.logger.info("Create Rich menu successful.")
