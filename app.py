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
from time import time

app = Flask(__name__)

line_bot_api = LineBotApi('JLeOUL8WbalfzEnZH8aRWLbD4CbFgj6fFeKCLLpLbBnuuZT49+uS81FM8o+ggVEw4pcGevHrHu5XnogwtqLiGiKlwacFAMXp0qps/uOKgpzCxIloOTln0dRawNY6z1gEHpo/vetBrc7eh4pKGFYjuwdB04t89/1O/w1cDnyilFU=') #チャンネルアクセストークン
handler = WebhookHandler('0c97dd986fc7bfe575ca8a33bf472dc9') #チャンネルシークレット

@app.route("/")
def test():
    return "OK"

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

users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    if event.message.text == "ありがとう":
        reply_message = "どういたしまして。"
    elif event.message.text == "好きな漫画は？":
         reply_message = "ドラゴンボール\nBLEACH\nクロスボーンガンダムです。"
    elif event.message.text == "計測開始":
        reply_message = "計測を開始しました"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0
        users[userId]["start"] = time()
    elif event.message.text == "計測終了":
        end = time()
        difference = int(end - users[userId]["start"])
        users[userId]["total"] += difference
        hour = difference // 3600
        minute = (difference % 3600) // 60
        second = difference % 60
        t_hour = users[userId]["total"] // 3600
        t_minute = (users[userId]["total"] % 3600) // 60
        t_second = users[userId]["total"] % 60
        reply_message = f"{hour}時間{minute}分{second}秒\n合計{t_hour}時間{t_minute}分{t_second}秒\n計測を終了しました"
    else:
        reply_message = "ひぃっ！"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = reply_message))


if __name__ == "__main__":
    app.run()