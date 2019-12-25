from . import MyBooks, QueryBooks, RenewBooks, RentReminder, ReserveBook
from .debug import adduser, lsuser
from flask import current_app as app

eventlist = [ MyBooks, QueryBooks, RentReminder, RenewBooks, ReserveBook ]

if app.config['DEBUG']:
    eventlist += [ adduser, lsuser ]

