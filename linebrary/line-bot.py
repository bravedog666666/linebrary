from flask import Flask, request, abort
import json

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FlexSendMessage,
    LocationMessage,
    LocationSendMessage,
    TemplateSendMessage,
    MessageTemplateAction,
    ButtonsTemplate,
    PostbackTemplateAction,
    URITemplateAction,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
)
import os
from readjson import readJSON
from publiclibrary import getCountyurl, getPublicbook, getResponse,getCategory
from booklibrary.mculibrary import book_url,getmculibrarylist,getmculibrarybook,getmculibraryjournal 
from math import radians, cos, sin, asin, sqrt
import bs4 as bs  # BeautifulSoup

app = Flask(__name__)

line_bot_api = LineBotApi(
    "xfIT5+Nb8I9Cp7tSoMM2/vPAaLSfpbEYh6gqqr+uqM6NbC/vcgNwWtt6xATUx6vvphaHYNgvO3IeUIubrDqr5WsEAz00Q3fE0mp9JOLFLOMxR8kQc/1AHN2fTtZ2eb+44GB1EFL3cIOgnG5bxVyraAdB04t89/1O/w1cDnyilFU="
)
handler = WebhookHandler("61118e74953d786cef6cda8926a3b472")

libraries = readJSON()
# print(libraries.get('library'))


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入欲查詢書名"))
    # bookname=event.message.text
    user_lat = event.message.latitude
    user_longitude = event.message.longitude
    lib = getlibrary(user_lat, user_longitude)
    publiclibrarybooklist = publiclibrary("小王子", lib.get("所屬縣市"))
    (mcubooklist,mcujournallist)=mculibrary("小王子")
    publiclibrarybook = getFlexMessage(publiclibrarybooklist)
    mcubook=getFlexMessage(mcubooklist)
    # mcujournal=getFlexMessage(mcubooklist)
    print(json.dumps(publiclibrarybook))
    print(json.dumps(mcubook))
    # publiclibrarybook=getCarouselColumn(publiclibrarybooklist)

    message = [
        TextSendMessage(text="搜尋書名為〈小王子〉"),
        LocationSendMessage(
            title=lib.get("圖書館名稱"),
            address=lib.get("地址"),
            latitude=lib.get("緯度"),  # 緯度
            longitude=lib.get("經度"),  # 經度
        ),
        # TextSendMessage(text="hello"),
        FlexSendMessage(alt_text="市立圖書館資訊", contents=publiclibrarybook),
        FlexSendMessage(alt_text="銘傳圖書", contents=mcubook)
    ]
    line_bot_api.reply_message(event.reply_token, message)


def getlibrary(user_lat, user_longitude):
    nearest_lib = sorted(
        libraries,
        key=lambda library: haversine(
            user_longitude, user_lat, library.get("經度"), library.get("緯度")
        ),
    )
    return nearest_lib[0]
    # librarylist=[library.get('圖書館名稱'),library.get('地址'),library.get('經度'),library.get('緯度') for library in libraries]


def haversine(lon1, lat1, lon2, lat2):  # 經度1，緯度1，經度2，緯度2 （十進制度數）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """

    # print('args:', lon1, lat1, lon2, lat2)
    # 將十進制度數轉化為弧度
    lon1, lat1, lon2, lat2 = map(
        radians, [float(lon1), float(lat1), float(lon2), float(lat2)]
    )

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半徑，單位為公里
    return c * r * 1000


# TextSendMessage(text=event.message.text)
def publiclibrary(book_name, County):
    # book_name="小王子"
    # ISBN="&search_input=978986189906&search_field=ISBN&"
    Category=getCategory(County)
    publicbook = getPublicbook(Category, County,book_name)
    return publicbook

def mculibrary(book_name):
    (book_list,journal_list)=getmculibrarylist(book_name)
    mcubook=getmculibrarybook(book_name,book_list)
    mcujournal=getmculibraryjournal(book_name,journal_list)
    return mcubook,mcujournal


def getFlexMessage(books):
    j = {
        "type": "carousel",
        "contents": list(map(book_map, books)),
    }
    # print(json.dumps(j))
    return j


def book_map(book):
    result = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": book.get("圖片"), 
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "2:3",
                    "gravity": "top",
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
                                    "text": book.get('書名'),
                                    "size": "lg",
                                    "color": "#ffffff",
                                    "weight": "bold",
                                    "style": "normal",
                                    "wrap": True,
                                }
                            ],
                        }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303Acc",
                    "paddingAll": "20px",
                    "paddingTop": "18px",
                    "height": "178px",
                },
            ],
            "paddingAll": "0px",
        },
    }

    content = [
        {
            "type": "text",
            "text": "作者：" + (book.get("作者") if book.get("作者") else "不詳"),
            "color": "#ebebeb",
            "size": "sm",
            "flex": 0,
            "margin": "none",
        },
        {
            "type": "text",
            "text": "ISBN：" + (book.get("ISBN") if book.get("ISBN") else "不詳"),
            "color": "#ebebeb",
            "size": "sm",
            "flex": 0,
            "margin": "none",
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "filler"},
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {"type": "filler"},
                        {
                            "type": "text",
                            "text": "詳細資訊",
                            "color": "#ffffff",
                            "flex": 0,
                            "offsetTop": "-2px",
                        },
                        {"type": "filler"},
                    ],
                    "spacing": "sm",
                },
                {"type": "filler"},
            ],
            "borderWidth": "1px",
            "cornerRadius": "4px",
            "spacing": "sm",
            "borderColor": "#ffffff",
            "margin": "md",
            "height": "40px",
            "action": {"type": "uri", "label": "action", "uri": book.get("網址")},
        }
    ]

    if content:
        content_result = {
            "type": "box",
            "layout": "vertical",
            "contents": content,
            "spacing": "lg",
            "margin": "xs",
        }
        result["body"]["contents"][1]["contents"].append(content_result)
    return result


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

