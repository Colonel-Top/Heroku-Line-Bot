from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('H1Zg2W7yWl5UP2BQ5wauI2Y5MzohU4oCvII7X2xsMn67lPuYsqRH2xNaHm18jCgKG+lQ3Bhnu5hrMmKcbjKlgrHxt0EEIzzgf9WedNE9E10zzWazC2Sd2QueFCrbfJ4ep9Et7oWsdueqw3cSNYPx6wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('872a89bf7e89a4ca43562a3f2e978a57')


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


if __name__ == "__main__":
    app.run()