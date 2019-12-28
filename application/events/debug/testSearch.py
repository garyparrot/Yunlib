from flask import current_app as app
from linebot.models import MessageEvent, TextMessage, FlexSendMessage
from ...models.users import User
from ... import db

flex_message = {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
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
        "text": "為什麼愛說謊",
        "size": "xs",
        "align": "end",
        "gravity": "bottom",
        "wrap": False,
        "color": "#888888",
        "margin": "xl"
      }
    ],
    "spacing": "none",
    "margin": "none",
    "paddingBottom": "10px"
  },
  "body": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          { "type": "text", "text": "標題", "weight": "bold" },
          { "type": "separator" },
          { "type": "separator", "margin": "md", "color": "#ffffff" },
          { "type": "text", "text": "Linux 黑魔法" },
          { "type": "text", "text": "hello, world" }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          { "type": "text", "text": "出版年", "align": "end", "weight": "bold" },
          { "type": "separator" },
          { "type": "separator", "margin": "md", "color": "#ffffff" },
          { "type": "text", "text": "2001", "align": "end" },
          { "type": "text", "text": "2005", "align": "end" }
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
          { "type": "text", "text": "2/2", "align": "end" },
          { "type": "text", "text": "0/2", "align": "end" }
        ],
        "flex": 0,
        "margin": "md"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "text",
        "text": "第n/m頁",
        "size": "sm",
        "gravity": "bottom",
        "offsetStart": "5px"
      },
      {
        "type": "text",
        "text": "下一頁",
        "flex": 0,
        "align": "end",
        "color": "#46abea",
        "size": "md",
        "action": {
          "type": "postback",
          "label": "action",
          "data": "hello"
        },
        "offsetEnd": "10px"
      }
    ]
  },
  "styles": {
    "header": {
      "backgroundColor": "#e6f7e8",
      "separator": False
    },
    "body": {
      "backgroundColor": "#ffffff"
    },
    "footer": {
      "separator": True,
      "separatorColor": "#eeeeee"
    }
  }
}

def checkEvent(args):
    return args.message.text.startswith("test")

def handleEvent(args):
    return FlexSendMessage(alt_text="Done", contents = flex_message)
