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

line_bot_api = LineBotApi('s64aQrnq8GLstmpABnVPkrieF1pQ+4TmXmSgKdYa5wL7IvfmDmYkkwEt7sDCKbAgn71KV68r8Oy3xPUskAqp0hFbZ+suJ7SeR7LgjOuVtQ4utOMNITpQlMPRfEpOiXsdVBUZixUbdf+Zcy5GgizgagdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dccc498b98db3e44e057811b26a96c7e')

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

from time import time
users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    if event.message.text == "勉強開始":
        reply_message = "計測を開始しました。"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] =0 
        users[userId]["start"] = time()
    else:
        end = time()
        difference = int(end - users[userId]["start"])
        users[userId]["total"] += difference
        hour = difference // 3600
        minute = (difference % 3600) // 60
        second = difference % 60
        users_hour = users[userId]['total'] // 3600
        users_minute = (users[userId]['total']) // 60
        users_second =  users[userId]['total'] % 60
        reply_message = f"ただいまの勉強時間は{hour}時間{minute}分{second}秒です。お疲れ様でした！合計で{users_hour}時間{users_minute}分{users_second}秒勉強しています。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()