from flask import Flask, request, abort
import os

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

#環境変数取得
ACCESS_TOKEN = "2rtnIH0XFLTP/P2/RDWGVhH/YyxCBqIbz4vZNNlLIJ7yZKVrTNCNTwYgWa528rzYF9ijKk6+KeLNVFlIZmN/KrFvF3RBm7hNEyM+nun7FYF3cLzS5bZ+AoVzrFZ0+oXaP/y2sQNd989UjNvh56j6iwdB04t89/1O/w1cDnyilFU="
SECRET = "a099cea6f830485870a134ea0a1e19e5"

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

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
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)