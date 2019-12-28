from . import MyBooks, QueryBooks, RenewBooks, RentReminder, ReserveBook, Auth
from .debug import adduser, lsuser, testSearch
from flask import current_app as app

eventlist = [ MyBooks, QueryBooks, RentReminder, RenewBooks, ReserveBook, Auth]

if app.config['DEBUG']:
    eventlist += [ adduser, lsuser, testSearch ]

