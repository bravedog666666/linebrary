from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction

CHANNEL_ACCESS_TOKEN = "61118e74953d786cef6cda8926a3b472"
to = "U39215b78d5d3d096fe23aad0d3730992"

line_bot_api = LineBotApi("xfIT5+Nb8I9Cp7tSoMM2/vPAaLSfpbEYh6gqqr+uqM6NbC/vcgNwWtt6xATUx6vvphaHYNgvO3IeUIubrDqr5WsEAz00Q3fE0mp9JOLFLOMxR8kQc/1AHN2fTtZ2eb+44GB1EFL3cIOgnG5bxVyraAdB04t89/1O/w1cDnyilFU=")

try:
    message = LocationSendMessage(
        title='101大樓',
        address='台北市信義路五段7號',
        latitude=25.034207,  #緯度
        longitude=121.564590  #經度
    )
   

    line_bot_api.push_message(to, message)
except:
    line_bot_api.push_message(to,TextSendMessage(text='發生錯誤！'))
    