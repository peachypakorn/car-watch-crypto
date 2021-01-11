from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests
import json
import os
import redis

def get_message_from_line(event,line_obj,redis_obj,input_text):
    if (input_text=="#price"):
        response = requests.get("https://api.bitkub.com/api/market/ticker")
        response_body = json.loads(response.text)
        interested = ["THB_BTC","THB_ETH","THB_XRP","THB_BCH","THB_OMG"]
        response_message = "Current Price :D\n"
        for i in interested:
            coin_data = response_body[i]
            response_message = response_message +"\n"+i+" latest price:"+ str(coin_data["last"])+" change:"+str(coin_data["percentChange"])+"%\n"

        line_obj.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message))

    elif(event.message.text[0]=="#"):
        line_obj.reply_message(
            event.reply_token,
            TextSendMessage(text="อย่าพึงทัก ยังทำไม่เสร็จ"))