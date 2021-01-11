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
import ast

def get_config_obj(event,redis_obj):
    config_obj = {}
    if (event.source.type=="group"):
        if redis_obj.exists(event.source.groupId):
            config_obj = ast.literal_eval(redis_obj.get(event.source.groupId).decode("utf-8"))
        config_obj["id"] = event.source.groupId
        
    elif(event.source.type=="user"):
        if redis_obj.exists(event.source.userId):
            config_obj = ast.literal_eval(redis_obj.get(event.source.userId).decode("utf-8)"))
        config_obj["id"] = event.source.userId

    return config_obj


def save_config_obj(config_obj,redis_obj):
    redis_obj.set(config_obj[id],str(config_obj))

def response_line(line_obj,event,response_message):
    line_obj.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message))

def get_message_from_line(event,line_obj,redis_obj,input_text):
    # config_obj = get_config_obj(event,redis_obj)
    config_obj = {}
    config_obj["id"] = event.source.userId
    response_line(line_obj,event,input_text +"  "+event.source.type+" "+event.source.userId+" "+str(redis_obj.exists(event.source.userId))+" "+str(config_obj) )






    if (input_text=="#price"):
        response = requests.get("https://api.bitkub.com/api/market/ticker")
        response_body = json.loads(response.text)
        interested = ["THB_BTC","THB_ETH","THB_XRP","THB_BCH","THB_OMG"]
        response_message = "Current Price :D\n"
        for i in interested:
            coin_data = response_body[i]
            response_message = response_message +"\n"+i+" latest price:"+ str(coin_data["last"])+" change:"+str(coin_data["percentChange"])+"%\n"
        response_line(line_obj,event,response_message)
        

    elif "#base" in input_text:
        if len(input_text) < 10:
            response_line(line_obj,event,"Syntax Error please try again")
        else:
            config_obj["base"][input_text[6:8]] = input_text[10:]
            save_config_obj(config_obj,redis_obj)
            response_line(line_obj,event,"Base added" + input_text[6:])

        # redis_obj.set(input_text[6:8],)        

    elif "#clearbase" in input_text:
        config_obj["base"] = []
        save_config_obj(config_obj,redis_obj)
        response_line(line_obj,event,"Base cleared")


    elif "#showbase" in input_text:
        response_line(line_obj,event,str(config_obj["base"]))


    elif(event.message.text[0]=="#"):
        line_obj.reply_message(
            event.reply_token,
            TextSendMessage(text="อย่าพึงทัก ยังทำไม่เสร็จ"))