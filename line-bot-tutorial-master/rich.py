import requests
import json
from linebot import (
    LineBotApi, WebhookHandler
)

headers = {"Authorization":"Bearer DJJQ1cqtdzeEdfylCE7xGdZaNE56/GSLQeJHTr3fSneI4uPqItEzInF06Bhr65zKc2lr3HFxhIFBRCNF9GhytL1cPPt6uJdU6lwxIF+dMgfMBVLV8RiDzc/JeJGnJOFQkdvFTgOYd5i2CoQU/0DsWAdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

line_bot_api = LineBotApi('DJJQ1cqtdzeEdfylCE7xGdZaNE56/GSLQeJHTr3fSneI4uPqItEzInF06Bhr65zKc2lr3HFxhIFBRCNF9GhytL1cPPt6uJdU6lwxIF+dMgfMBVLV8RiDzc/JeJGnJOFQkdvFTgOYd5i2CoQU/0DsWAdB04t89/1O/w1cDnyilFU=')

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "Controller",
    "areas":[
        {
          "bounds": {"x": 280, "y": 185, "width": 520, "height": 655},
          "action": {"type": "message", "text": "續借"}
        },
        {
          "bounds": {"x": 280, "y": 935, "width": 520, "height": 655},
          "action": {"type": "message", "text": "right"}
        },
        {
          "bounds": {"x": 1000, "y": 185, "width": 520, "height": 655},
          "action": {"type": "message", "text": "辭典"}
        },
        {
          "bounds": {"x": 1000, "y": 935, "width": 520, "height": 655},
          "action": {"type": "message", "text": "left"}
        },
        {
          "bounds": {"x": 1725, "y": 185, "width": 520, "height": 655},
          "action": {"type": "message", "text": "btn b"}
        },
        {
          "bounds": {"x": 1725, "y": 935, "width": 520, "height": 655},
          "action": {"type": "message", "text": "btn a"}
        }
    ]
  }
#建立新的rich_menu 將上面設定的版面(body)放置post 使用print(req.text)來看新創的rich_menu_id  
#req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',headers=headers,data=json.dumps(body).encode('utf-8'))

#上傳圖片至已設好的richmenu 圖片有限定格式 大小2500:1686 ;2500 843 檔案類型 jpeg/png 檔案大小<1M 
with open("D:\專研用\line-bot-tutorial-master/imm.jpeg", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-920027d72b62ba2f30b1546110b71d53", "image/jpeg", f)


#將設置好的內容重新上傳
req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-920027d72b62ba2f30b1546110b71d53', headers=headers)

#刪除以建立過的表單
#line_bot_api.delete_rich_menu('richmenu-458d989482c6e894c5f3c2d4055ef9c3')

print(req.text)
