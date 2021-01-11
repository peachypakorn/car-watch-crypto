# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

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
import controller


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

line_bot_api = LineBotApi("Xre38PQd9ZBFQiaC7oQ92TuafYlNFCVJDQ/t93iDpkjeHDW0CjnJqGf7CKQOv3dfrDnfTd9YlRrrCPAMac2zK6DBee/gUYTcN/wdWR66Q1uIFwHxiUKrYs1KxcU2jNMGqKLwu42gQ/R5zzeoF1DnfQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler('8f92c499e40a9710beeaba30af98babd')
redis_obj = redis.Redis(host='redis-18376.c3.eu-west-1-2.ec2.cloud.redislabs.com',port=18376, db=0,password='06x6jL6C54f5yYR4ctQEwYLROEn6V1vf')
redis_obj.set('peachy','pakorn')
print(redis_obj.get('peachy'))

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    controller.get_message_from_line(event,line_bot_api,redis_obj,event.message.text)
    
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=event.message.text))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


    # {"id":1,"last":1229999,"lowestAsk":1229999,"highestBid":1225999,"percentChange":-1.44,"baseVolume":657.29056115,
    # "quoteVolume":811822485.63,"isFrozen":0,"high24hr":1260000,"low24hr":1183005,"change":-18000.99,"prevClose":1229999,
    # "prevOpen":1247999.99}