import json
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage
from math import floor, ceil, ceil
from flask import current_app as app
from .. import linebot, webhook
from ..crawlers.QueryBooks import BookQuery, crawler, BookDetail, bookDetailCrawler

def checkEvent(args):
    return args.message.text.startswith("搜尋")

isQuerybook  = lambda postback: postback["type"] == "querybook"
isBookdetail = lambda postback: postback["type"] == "bookdetail"

def checkPostback(args):
    postback = json.loads(args.postback.data)


    return isQuerybook(postback) or isBookdetail(postback) 

def handleEvent(args):

    if args.message.text.startswith("搜尋?"):
        return helpme(args)

    return startQuery(args.message.text)

def handlePostback(args):

    postback = json.loads(args.postback.data)

    if isQuerybook(postback):
        return startQuery(postback["query"])
    elif isBookdetail(postback):
        return startQueryDetail(postback["query"])

"""
從給定字串命令進行圖書查詢
"""
def startQuery(command):
# {{{
    command = command.split(' ')
    command = [ cmd for cmd in command if cmd != "" ]
    query = BookQuery(sortby = "PUBLISH_YEAR_DOWN")

    iters = iter(command)
    try:
        # TODO but I don't want to do, This parser have ambiguous grammar.
        # These code is a tragedy, serious.
        isBooknameLast = False
        isAuthorLast = False
        for item in iters:

            breakLast = True

            if item == "搜尋":
                query.bookname = next(iters)
                isBooknameLast, isAuthorLast, breakLast = True, False, False
            elif item == "搜尋ISBN" or item == "ISBN":
                query.ISBN = next(iters)
            elif item == "搜尋索書號" or item == "索書號":
                query.bookid = next(iters)
            elif item == "搜尋ISSN" or item == "ISSN":
                query.ISSN = next(iters)
            elif item == "搜尋作者" or item == "作者":
                query.author = next(iters)
                isBooknameLast, isAuthorLast, breakLast = False, True, False
            elif item == "書名排序":
                query.sortby = "TITLE"
            elif item == "索書號排序":
                query.sortby = "MARC_CLASS"
            elif item == "出版年升冪":
                query.sortby = "PUBLISH_YEAR_UP"
            elif item == "出版年降冪":
                query.sortby = "PUBLISH_YEAR_DOWN"
            elif item[0] == "~" and item[1:].isdigit():
                query.startAt = int(item[1:])
            elif isBooknameLast:
                query.bookname += " " + item
                breakLast = False
            elif isAuthorLast:
                query.author += " " + item
                breakLast = False
            else:
                return helpme(args)

            if breakLast:
                isBooknameLast = False
                isAuthorLast = False
    except:
        pass

    result = crawler(query)

    if type(result) is tuple:
        message = create_booklist(result[0], query.startAt, result[1], " ".join(command[1:]), command)
        print(message)
        return FlexSendMessage(alt_text = "搜尋 " + query.bookname, contents = message)
    elif type(result) is BookDetail:
        return FlexSendMessage(alt_text=str(result), contents = create_bookdetail(result)) 
    else:
        return TextSendMessage(text="鵝... 什麼都沒有") # }}}

def startQueryDetail(site):
    bookdetail = bookDetailCrawler(ssite = site)# {{{
    message    = create_bookdetail(bookdetail)
    return FlexSendMessage(alt_text = str(bookdetail), contents = message) # }}}

def create_bookdetail(book):
# {{{
    def generate_entry(label, value):
        label = str(label)
        value = str(value)
        label = " " if len(label) == 0 else label
        value = " " if len(value) == 0 else value
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                { "type": "text", "text": f"{str(label)}：", "flex": 0, "size": "sm", "weight": "bold" },
                { "type": "text", "text": f"{str(value)}", "size": "sm", "margin": "md", "maxLines": 3, "align": "end" }
            ] 
        }

    translator = {
        "accessionNo":     "登錄號",
        "callNo":          "索書號",
        "type":            "特藏類型",
        "purpose":         "特定用途",
        "location":        "館藏地點",
        "bookstatus":      "圖書狀況",
        "duedate":         "借書到期日",
        "reserved amount": "預約人數",
    }

    return {
          "type": "bubble",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [ { "type": "text", "text": str(book.bookname), "weight": "bold" } ],
            "paddingBottom": "10px",
            "backgroundColor": "#e6f7e8"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                *([ generate_entry(key, value) for key, value in book.bookinfo.items() ] if book.bookinfo else []),
                # separator cannot be the last element in box component! so we have to validity if there is something under it
                *([{ "type": "separator", "margin": "xl" }, { "type": "separator", "margin": "xl", "color": "#ffffff" }] if book.bookstatus else [] ),
                *([ generate_entry(translator[key], value) for key, value in book.bookstatus.items() ] if book.bookstatus else []),
            ]
          }
    }# }}}

def create_booklist(table, result_index, record_amount, title, command):
    page_size = app.config['PAGE_SIZE']# {{{
    bookname = [ str(item[1][1]) for item in table.iterrows() ][:page_size]
    pubyear  = [ str(item[1][3]) for item in table.iterrows() ][:page_size]
    amount   = [ str(item[1][6]) for item in table.iterrows() ][:page_size]
    url      = [ str(item[1]["url"]) for item in table.iterrows() ][:page_size]
    command = command if command[-1][0] != '~' and not command[-1][1:].isdigit() else command[:-1]
    next_page = " ".join(command + [ f"~{result_index + page_size}" ])

    isLastPage = result_index + page_size >= record_amount
    action = {"action": { "type": "postback", "label": "下一頁", "data": '{"type": "querybook", "query": "%s" }' % next_page }}
    
    def create_entry_action(bookname, url):
        return {"action": { "type": "postback", "label": f"詳細訊息", "data": '{"type": "bookdetail", "query": "%s"}' % url }}

    return {
      "type": "bubble",
      "header": {
        "type": "box",# {{{
        "layout": "horizontal",
        "contents": [
          {# {{{
            "type": "text",
            "text": "搜尋結果",
            "color": "#29b23f",
            "weight": "regular",
            "size": "lg",
            "align": "start",
            "flex": 0
          },
          {
            "type": "text",
            "text": str(title),
            "size": "xs",
            "align": "end",
            "gravity": "bottom",
            "wrap": False,
            "color": "#888888",
            "margin": "xl"
          }# }}}
        ],
        "spacing": "none",
        "margin": "none",
        "paddingBottom": "10px"# }}}
      },
      "body": {
        "type": "box",# {{{
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              { "type": "text", "text": "標題", "weight": "bold" },
              { "type": "separator" },
              { "type": "separator", "margin": "md", "color": "#ffffff" },
              *[ {"type": "text", "text": str(bookname[index]), **create_entry_action(bookname[index], url[index]) } for index in range(len(bookname)) ]
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              { "type": "text", "text": "出版年", "align": "end", "weight": "bold" },
              { "type": "separator" },
              { "type": "separator", "margin": "md", "color": "#ffffff" },
              *[ {"type": "text", "text": text.split('.',1)[0], "align": "end" } for text in pubyear ]
            ],
            "flex": 0,
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              { "type": "text", "text": "數量", "weight": "bold", "align": "end" },
              { "type": "separator" },
              { "type": "separator", "margin": "md", "color": "#ffffff" },
              *[ {"type": "text", "text": text, "align": "end" } for text in amount ]
            ],
            "flex": 0,
            "margin": "md"
          }
        ]# }}}
      },
      "footer": {
        "type": "box",# {{{
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "第%d/%d頁" % ( floor(result_index / page_size) + 1, ceil(record_amount / page_size )) ,
            "size": "sm",
            "gravity": "bottom",
            "offsetStart": "5px"
          },
          { "type": "text",
            "text": "下一頁" if not isLastPage else "最後一頁",
            "flex": 0,
            "align": "end",
            "color": "#46abea" if not isLastPage else "#555555",
            "size": "md",
            **( action if not isLastPage else {} ),
            "offsetEnd": "10px"
          }
        ]# }}}
      },
      "styles": {
        "header":   { "backgroundColor": "#e6f7e8", "separator": False },# {{{
        "body":     { "backgroundColor": "#ffffff" },
        "footer":   { "separator": True, "separatorColor": "#eeeeee" }# }}}
      }
    }# }}}


def helpme(args):
    help_message = {
                # {{{
                  "type": "bubble",
                  "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "搜尋書籍功能",
                        "weight": "regular",
                        "size": "lg"
                      }
                    ],
                    "paddingBottom": "10px"
                  },
                  "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "搜尋書名",
                            "flex": 0,
                            "weight": "regular"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "text",
                            "text": "搜尋 <書名> [選項] ...",
                            "size": "xs",
                            "gravity": "bottom",
                            "align": "end",
                            "margin": "md",
                            "color": "#666666"
                          }
                        ],
                        "margin": "md"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "搜尋ISBN",
                            "flex": 0,
                            "weight": "regular"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "text",
                            "text": "搜尋ISBN <ISBN> [選項] ...",
                            "size": "xs",
                            "gravity": "bottom",
                            "align": "end",
                            "margin": "md",
                            "color": "#666666"
                          }
                        ],
                        "margin": "md"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "搜尋索書號",
                            "flex": 0,
                            "weight": "regular"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "text",
                            "text": "搜尋索書號 <圖書館索書號> [選項] ...",
                            "size": "xs",
                            "gravity": "bottom",
                            "align": "end",
                            "margin": "md",
                            "color": "#666666"
                          }
                        ],
                        "margin": "md"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "搜尋期刊",
                            "flex": 0,
                            "weight": "regular"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "text",
                            "text": "搜尋ISSN <期刊ISSN> [選項] ...",
                            "size": "xs",
                            "gravity": "bottom",
                            "align": "end",
                            "margin": "md",
                            "color": "#666666"
                          }
                        ],
                        "margin": "md"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "搜尋作者",
                            "flex": 0,
                            "weight": "regular"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "text",
                            "text": "搜尋作者 <作者名稱> [選項] ...",
                            "size": "xs",
                            "gravity": "bottom",
                            "align": "end",
                            "margin": "md",
                            "color": "#666666"
                          }
                        ],
                        "margin": "md"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                          {
                            "type": "text",
                            "text": "可用選項"
                          },
                          {
                            "type": "separator"
                          },
                          {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                              {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                  {
                                    "type": "text",
                                    "text": "書名排序：對書名進行字典序排序",
                                    "size": "xs",
                                    "gravity": "bottom",
                                    "align": "start",
                                    "margin": "md",
                                    "color": "#666666",
                                    "wrap": True
                                  },
                                  {
                                    "type": "text",
                                    "text": "索書號排序：對索書號進行排序",
                                    "size": "xs",
                                    "gravity": "bottom",
                                    "align": "start",
                                    "margin": "md",
                                    "color": "#666666",
                                    "wrap": True
                                  },
                                  {
                                    "type": "text",
                                    "text": "出版年升冪：舊書優先顯示",
                                    "size": "xs",
                                    "gravity": "bottom",
                                    "align": "start",
                                    "margin": "md",
                                    "color": "#666666",
                                    "wrap": True
                                  },
                                  {
                                    "type": "text",
                                    "text": "出版年降冪：新書優先顯示(預設)",
                                    "size": "xs",
                                    "gravity": "bottom",
                                    "align": "start",
                                    "margin": "md",
                                    "color": "#666666",
                                    "wrap": True
                                  }
                                ],
                                "margin": "xxl",
                                "offsetStart": "15px"
                              }
                            ],
                            "margin": "lg"
                          }
                        ],
                        "margin": "xxl"
                      }
                    ]
                  },
                  "styles": {
                    "header": {
                      "separator": True
                    },
                    "body": {
                      "backgroundColor": "#f3f3f3"
                    }
                  }
                # }}}
    }

    return FlexSendMessage(alt_text = "help", contents = help_message)
