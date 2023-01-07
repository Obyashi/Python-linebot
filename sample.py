from django.http import HttpResponseForbidden, HttpResponse

from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, FollowEvent, UnfollowEvent,
    TextSendMessage, ImageMessage, AudioMessage
)

from linebot import LineBotApi, WebhookHandler


# 各クライアントライブラリのインスタンス作成
line_bot_api = LineBotApi(channel_access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=LINE_ACCESS_SECRET)


def callback(request):
    # signatureの取得
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('Shift-JIS')
    try:
        # 署名の検証を行い、成功した場合にhandleされたメソッドを呼び出す
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    return HttpResponse('OK')



# フォローイベントの場合の処理
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='初めまして')
    )


# メッセージイベントの場合の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # メッセージでもテキストの場合はオウム返しする
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

@handler.add(MessageEvent, message=(ImageMessage, AudioMessage))
def handle_image_audio_message(event):
    # 画像と音源の場合は保存する
    content = line_bot_api.get_message_content(event.message.id)
    with open('file', 'w') as f:
        for c in content.iter_content():
            f.write(c)