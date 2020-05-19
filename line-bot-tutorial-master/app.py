# encoding: utf-8
import os
import agent
import configparser
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, URITemplateAction, TextSendMessage,
    FlexSendMessage, BubbleContainer, ImageComponent, URIAction
)
config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__)

# 填入你的 message api 資訊
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# 設定你接收訊息的網址，如 https://YOURAPP.herokuapp.com/callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@app.route('/')
def index():
    return 'Hello World'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    # content = "{}: {}".format(event.source.user_id, event.message.text)
    t, i = agent.dialogflow_library_agent(event.message.text)
    #if i == 'LINE_function_dictionary辭典功能':
           
    if i == 'library.agent.how.renew如何續借':
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={}
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=t+"\uDBC0\uDC79"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])
