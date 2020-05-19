import requests
import json
from linebot import (
    LineBotApi, WebhookHandler
)
headers = {"Authorization":"Bearer DJJQ1cqtdzeEdfylCE7xGdZaNE56/GSLQeJHTr3fSneI4uPqItEzInF06Bhr65zKc2lr3HFxhIFBRCNF9GhytL1cPPt6uJdU6lwxIF+dMgfMBVLV8RiDzc/JeJGnJOFQkdvFTgOYd5i2CoQU/0DsWAdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "Controller",
    "areas":[
        {
          "bounds": {"x": 551, "y": 325, "width": 321, "height": 321},
          "action": {"type": "message", "text": "up"}
        },
        {
          "bounds": {"x": 876, "y": 651, "width": 321, "height": 321},
          "action": {"type": "message", "text": "right"}
        },
        {
          "bounds": {"x": 551, "y": 972, "width": 321, "height": 321},
          "action": {"type": "message", "text": "down"}
        },
        {
          "bounds": {"x": 225, "y": 651, "width": 321, "height": 321},
          "action": {"type": "message", "text": "left"}
        },
        {
          "bounds": {"x": 1433, "y": 657, "width": 367, "height": 367},
          "action": {"type": "message", "text": "btn b"}
        },
        {
          "bounds": {"x": 1907, "y": 657, "width": 367, "height": 367},
          "action": {"type": "message", "text": "btn a"}
        }
    ]
  }

line_bot_api = LineBotApi('DJJQ1cqtdzeEdfylCE7xGdZaNE56/GSLQeJHTr3fSneI4uPqItEzInF06Bhr65zKc2lr3HFxhIFBRCNF9GhytL1cPPt6uJdU6lwxIF+dMgfMBVLV8RiDzc/JeJGnJOFQkdvFTgOYd5i2CoQU/0DsWAdB04t89/1O/w1cDnyilFU=')

with open("control.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-0aa73de23358809c1a209b7f67af9b5f", "alfons-morales-YLSwjSy7stw-unsplash_resized (1).jpg", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-0aa73de23358809c1a209b7f67af9b5f', 
                       headers=headers)

print(req.text)