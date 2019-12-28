import pandas as pd

import requests
from flask import current_app as app
from bs4 import BeautifulSoup


class BookQuery: # BookQuery {{{ #

    def __init__(self, **kargs):
        self.bookname = kargs.get('bookname',"")
        self.ISBN = kargs.get('ISBN', None)
        self.bookid = kargs.get('bookid', None)
        self.ISSN = kargs.get('ISSN', None)
        self.author = kargs.get('author', None)
        self.sortby = kargs.get('sortby', "TITLE")
        self.select = kargs.get('select', "TITLE")
        self.startAt = kargs.get('startAt', 0)

    def asPayload(self, transkey):
        payload = {}
        if self.bookname:   payload['KEYWORD'] = self.bookname.encode('big5')
        if self.ISBN:       payload['ISBN'] = self.ISBN
        if self.bookid:     payload['SSNO'] = self.bookid
        if self.ISSN:       payload['ISSN'] = self.ISSN
        if self.author:     payload['AUTHOR'] = self.author.encode('big5')
        if self.sortby:     payload['SortType'] = self.sortby
        if self.select:     payload['SELECTKEY'] = self.select
        if transkey:        payload['transkey'] = transkey

        return payload

# }}} BookQuery #

class BookDetail: # BookDetail {{{ #
    def __init__(self, info_table, status_table):
        self.bookinfo   = {}
        self.bookstatus = {}

        # Parse Book/Media information
        if info_table is not None:
            info_table   = info_table.fillna("")

            for index, row in info_table.iterrows():
                self.bookinfo[row[0]] = row[1]

            self.bookname = info_table.iloc[0][1]

        # Parse Book/Media Status
        if status_table is not None:
            status_table = status_table.fillna("")
            self.bookstatus = {
                "accessionNo":      status_table.iloc[0][1],
                "callNo":           status_table.iloc[0][2],
                "type":             status_table.iloc[0][3],
                "purpose":          status_table.iloc[0][4],
                "location":         status_table.iloc[0][5],
                "bookstatus":       status_table.iloc[0][6],
                "duedate":          status_table.iloc[0][7],
                "reserved amount":  status_table.iloc[0][8],
            }

    def __repr__(self):
        return f"<BookDetail {self.bookname}>"

# }}} BookDetail #

def crawler(query):

    # Obtain transkey
    site = "http://www.libwebpac.yuntech.edu.tw/Webpac2/msearch.dll/"
    session = requests.session()
    response =session.get(site)
    response.encoding = 'big5'
    transkey = BeautifulSoup(response.text, "html5lib").find( type = 'hidden' )['value']
    print("Key:", transkey)


    # Start query and obtain redirect location
    site = "http://www.libwebpac.yuntech.edu.tw/Webpac2/msearch.dll/BROWSE"
    response = session.post(site, data = query.asPayload(transkey))
    response.encoding ='big5'

    if "store.dll" in response.url:
        transkey = response.url.split("store.dll/?")[1]
        return bookDetailCrawler(session, transkey)
    elif "booklist.dll" in response.url:
        transkey = response.url.split('?P=-1&')[1]
        return booklistCrawler(session, query.startAt , transkey)
    else:
        return None

"""
針對搜尋結果清單設計的爬蟲
"""
def booklistCrawler(session, startAt, transkey): # {{{
    # Start fetching query length
    site = "http://www.libwebpac.yuntech.edu.tw/Webpac2/booklist.dll/?P=" + str(startAt) + "&" + transkey
    response = session.get(site)
    response.encoding = 'big5'
    soup = BeautifulSoup(response.text, "html5lib")

    total_records = int(str(soup.find("td", { "class": "td2" }).contents[0]).split("筆")[0])

    # Fetching Url of each entries
    table = soup.find_all("table")[1]
    url_value = table.select("tbody tr td:nth-of-type(2) a")
    urls = [ "http://www.libwebpac.yuntech.edu.tw/Webpac2/%s" % item["href"][3:] for item in url_value ]

    # Fetching content
    table = pd.read_html(response.text)[1]
    table.insert(7, "url", urls)
    table.fillna("")

    return table, total_records
# }}}

"""
針對書籍詳細資料設計的爬蟲
"""
def bookDetailCrawler(session = None, transkey = None, ssite = None): # {{{
    # Start fetching 
    if not session: session = requests.session()
    site = "http://www.libwebpac.yuntech.edu.tw/Webpac2/store.dll/?" + transkey if transkey else ssite
    response = session.get(site)
    response.encoding = 'big5'
    print(response.text)

    tables = pd.read_html(response.text)
    bookinfo   = tables[0] if len(tables) > 0 else None
    # Because of that page has a useless table on the buttom side of page.
    # we add a string check to ensure we didn't fetch the wrong one if the table is not exist
    # I know this code looks very weird, but to be honest the real weird one is the website itself.
    # Back to the network stone age, at that moment <nav> tag does not exist, so they use table instead.
    print(tables[1].head())
    bookstatus = tables[1] if len(tables) > 1 and not tables[1].empty else None         
    
    return BookDetail(bookinfo, bookstatus)
# }}}

if __name__ == "__main__":
    query = BookQuery(bookname = "你好")
    print(crawler(query))
