from django.http import HttpResponseForbidden, HttpResponse

from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, FollowEvent, UnfollowEvent,
    TextSendMessage, ImageMessage, AudioMessage
)

from linebot import LineBotApi, WebhookHandler

line_bot_api = LineBotApi(channel_access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=LINE_ACCESS_SECRET)


def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('Shift-JIS')
    try:
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

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

@handler.add(MessageEvent, message=(ImageMessage, AudioMessage))
def handle_image_audio_message(event):
    content = line_bot_api.get_message_content(event.message.id)
    with open('file', 'w') as f:
        for c in content.iter_content():
            f.write(c)