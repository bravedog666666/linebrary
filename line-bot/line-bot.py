from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,LocationMessage,LocationSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('xfIT5+Nb8I9Cp7tSoMM2/vPAaLSfpbEYh6gqqr+uqM6NbC/vcgNwWtt6xATUx6vvphaHYNgvO3IeUIubrDqr5WsEAz00Q3fE0mp9JOLFLOMxR8kQc/1AHN2fTtZ2eb+44GB1EFL3cIOgnG5bxVyraAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('61118e74953d786cef6cda8926a3b472')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    message=LocationSendMessage(
        title=event.message.title,
        address=event.message.address,
        latitude=event.message.latitude,  #緯度
        longitude=event.message.longitude  #經度
        )
    line_bot_api.reply_message(event.reply_token,message)


#TextSendMessage(text=event.message.text)


if __name__ == "__main__":
    app.run()