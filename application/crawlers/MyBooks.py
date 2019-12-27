import pandas as pd

from flask import current_app as app
from .ParseError import ParseError
from .Authentication import auth
from bs4 import BeautifulSoup

from .models.BorrowedBook import BorrowedBook

def crawler(username, password, site = "http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll"):

    session, transkey = auth(username, password, site)

    # Retrieve page of borrowed books
    mybook_url = f"{site}/BORROW?{transkey}"
    response = session.get(mybook_url)
    response.encoding = "big5"

    # Transform table in the page into pandas table 
    try:
        booktable = pd.read_html(response.text)[2]
        booktable = rearrange(booktable)
    except Exception as e:
        raise ParseError("Failed to parse data from table", response.text) from e

    # return result 
    return [BorrowedBook(book) for index, book in booktable.iterrows()]

# Rearrange the table so it looks better
def rearrange(table):
    table = table.drop(columns = [0,1])
    table = table.rename(columns = table.iloc[0])
    table = table.drop(index = [0])
    table = table.fillna("")

    return table

