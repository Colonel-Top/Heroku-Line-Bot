'''from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from linebot.exceptions import LineBotApiError
app = Flask(__name__)

line_bot_api = LineBotApi('QWiSqwAAs1/FyPo+Rt+jKoxjjK+LbkQ1pC1zsmCO9s5g2YO9EFUsSKO90ABQpc8h31iecVkjMsG3IZ2J9xCcS5pHL0ph8nc81PIM+gJEFzkJpHIRBWiJQl7sh6dOuuApuPMC+aj1HjkT5iaHCXDJ5AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('888960969fc0ebb0bc365fc194e97dc9')


try:
    line_bot_api.reply_message('<reply_token>', TextSendMessage(text='Hello World!'))
except  LineBotApiError as e:
    abort(400)
    print('error')
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
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@app.route('/')
def index():
    return 'OK ya!'
if __name__ == "__main__":
    app.run()'''
from flask import Flask, request
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"
# ส่วน callback สำหรับ Webhook
@app.route('/callback', methods=['POST'])
def callback():
    json_line = request.get_json()
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    user = decoded["events"][0]['replyToken']
    #id=[d['replyToken'] for d in user][0]
    #print(json_line)
    print("ผู้ใช้：",user)
    sendText(user,'งง') # ส่งข้อความ งง
    return '',200

def sendText(user, text):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = '888960969fc0ebb0bc365fc194e97dc9' # ใส่ ENTER_ACCESS_TOKEN เข้าไป

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = json.dumps({
        "replyToken":user,
        "messages":[{
            "type":"text",
            "text":text
        }]
    })

    #print("ข้อมูล：",data)
    r = requests.post(LINE_API, headers=headers, data=data) # ส่งข้อมูล
    #print(r.text)

if __name__ == '__main__':
    app.run(debug=True)