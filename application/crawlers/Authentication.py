from bs4 import BeautifulSoup
from ParseError import ParseError
import requests

def auth(username, password, site = "http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll"):
    payloads = {
            "COP": "SELF",
            "RNO": username,
            "PWD": password,
            "SEND": "確  定"
            }
    headers = { 
            "Host":             "www.libwebpac.yuntech.edu.tw",
            "Accept-Encoding":  "gzip, deflate",
            "Content-Type":     "application/x-www-form-urlencoded",
            "Origin":           "http://www.libwebpac.yuntech.edu.tw",
            "Connection":       "keep-alive",
            "Referer":          "http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll/",
            "Upgrade-Insecure-Requests": "1",
            "Pragma":           "no-cache",
            "Cache-Control":    "no-cache",
            }

    # Login website and retrieve transkey
    login_url = f"{site}/login"
    session  = requests.session()
    response = session.post(login_url, data = payloads, headers = headers)
    response.encoding = "big5"

    nav_url = retrieve_nav_url(response)

    # Retrieve transkey and other stuff
    headers = {
            "Host": "www.libwebpac.yuntech.edu.tw",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": "http://www.libwebpac.yuntech.edu.tw/Webpac2/Person.dll/login",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
    }

    nav_url  = f"{site}/{nav_url}"
    response = session.get(nav_url, headers = headers)
    response.encoding = "big5"

    transkey = retrieve_transkey(response)

    return session, transkey

"""
Retrieve Navbar anchor link from page
"""
def retrieve_nav_url(response):

    parser = BeautifulSoup(response.text, "html.parser")
    script = parser.find_all("script")

    if len(script) > 1 and "您的證號不正確" in script[2]:
        raise Exception("Login Failed.")

    navigator = parser.find("frame", { "name": "nav" })

    if not navigator.has_attr('src') or navigator['src'].find('?') == -1:
        raise PraseError("Unable to retrieve transkey ", response.text) 

    return navigator['src'][navigator['src'].find('/NAV?')+1:]

"""
Retrieve transkey 
"""
def retrieve_transkey(response):
    try:
        parser = BeautifulSoup(response.text, "html.parser")
        anchor = parser.select("ul > li > a")[0]
        transkey = anchor["href"][anchor["href"].find("?transkey") + 1 :]
        return transkey
    except Exception as e:
        raise ParseError("Failed to parse transkey", response.text) from e

