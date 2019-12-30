import time, datetime, atexit, os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app as app
from .crawlers.MyBooks import crawler
from .models.users import User
from .linemodels.booklist import MyBooklistRender, config as RenderConfig
from datetime import datetime, timedelta
from . import linebot
from linebot.models import FlexSendMessage, TextSendMessage
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from . import db

checkBookDuedate_delay = 3600

def checkBookDuedate(db_url):
    # check book due date every hour, but never send a notification during 9 pm to 8 am
    current = datetime.now()

    if current.hour <= 8 and current.hour < 21:
        print("Start due time checking...")

        # create database engine
        db = create_engine(db_url)
        
        # for each user test if their have book about to due
        query = "SELECT userid, lib_username, lib_password FROM user"
        for userid, username, password in db.execute(query):
            print("Scanning user: ", userid)

            # craw for its book
            books = crawler(username, password)

            # if any book is is about to due (3 days as a threshold), send notification
            if any([ book.due(datetime.now() + timedelta(days=3)) for book in books]):
                print("Userid: %s better return its book." % userid)

                config = RenderConfig(**{
                        "lfooter": f"共{len(books)}本書",
                        "rfooter": f"處理時間: {datetime.now().strftime('%m/%d %H:%M')}",
                        "books": books,
                        "title": f"{username}的到期提示",
                        "emptyhint": "你沒有借任何書:( ... What?"
                })
                flexMessage = MyBooklistRender(config = config).render()
                linebot.push_message(userid, FlexSendMessage(alt_text = "Mybooks", contents = flexMessage))
                linebot.push_message(userid, TextSendMessage(text="提醒您，有書要到期了"))

                # app.logger.info("Userid: %s got the messages.", userid)

        print("Done")

# Thread for job schedules
_already_started = False
def startScheduler():

    if _already_started:
        raise Exception("You cannot the scheduler twice.")

    # Flask-Sqlalchemy provide some hack with the database URL, so the sqlite database end up in the application dir (apply_driver_hacks)
    # Now we have to hack it too R$#DRQWER#%$CT%VGWRVEQWREQW WTF.
    URL = make_url(os.environ['SQLALCHEMY_DATABASE_URI'])
    db.make_connector(app, None).get_options(URL, False)

    app.logger.info("Start scheduler.")
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func = checkBookDuedate, trigger="interval", seconds = checkBookDuedate_delay, args = [ URL ])
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
