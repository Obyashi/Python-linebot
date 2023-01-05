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
import os

#Token�擾

YOUR_CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"
YOUR_CHANNEL_SECRET = "YOUR_CHANNEL_SECRET"

app = Flask(__name__)
app.debug = False

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
    df_list = [
        ['Google','https://www.google.com/'],
        ['yahoo','https://www.yahoo.co.jp/'],
        ]

    for i in range(len(df_list)):
        url = None
        if event.message.text == df_list[i][0]:
            url = df_list[i][1]
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=url)
                )
        else:
            continue

        if url == None:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='���̂悤�ȃT�C�g�͑��݂��܂���')
                )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
