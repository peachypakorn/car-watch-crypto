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
    if (event.message.text=="#price"):
        response = requests.get("http://api.open-notify.org/this-api-doesnt-exist")
        interested = ['THB_BTC',"THB_ETH","THB_XRP","THB_BCH","THB_OMG"]
        response_message = "Current Price :D"
        for i in interested:
            coin_data = response.json()[i]
            response_message = response_message +"/n"+i+" lastest price:"+ coin_data["last"]+" change:"+coin_data["percentChange"]+"/n"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message))

    elif(event.message.text[0]=="#"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="อย่าพึงทัก ยังทำไม่เสร็จ"))
        # line_bot_api.reply_message(
        #     event.reply_token,
        #     TextSendMessage(text=event.message.text))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


    # {"id":1,"last":1229999,"lowestAsk":1229999,"highestBid":1225999,"percentChange":-1.44,"baseVolume":657.29056115,
    # "quoteVolume":811822485.63,"isFrozen":0,"high24hr":1260000,"low24hr":1183005,"change":-18000.99,"prevClose":1229999,
    # "prevOpen":1247999.99}