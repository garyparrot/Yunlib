from datetime import datetime

class BorrowedBook:

    """Data structure to describe the book user borrowed"""

    # Em.... Is this code useless?
    # Whatever we ignore it for this moment.
    def __init__(self, bookname, author, duedate, renew_counter = 0, reservation_counter = 0, note = "", library_name = ""):
        self.library_name = ""
        self.bookname = bookname
        self.author = author
        self.duedate = duedate
        self.duedate_time = datetime.strptime(duedate, "%Y/%m/%d")
        self.renew_counter = renew_counter 
        self.reservation_counter = reservation_counter
        self.note = note

    def __init__(self, row):
        self.library_name           = row[0]
        self.bookname               = row[1]
        self.author                 = row[2]
        self.duedate                = row[3]
        self.duedate_time = datetime.strptime(self.duedate, "%Y/%m/%d")
        self.renew_counter          = row[4]
        self.reservation_counter    = row[5]
        self.note                   = row[6]

    def due(self, time):
        return self.duedate_time < time

    def __repr__(self):
        return f"<Book \'{self.bookname[:10]}{'...' if len(self.bookname) > 10 else ''}\'>"
