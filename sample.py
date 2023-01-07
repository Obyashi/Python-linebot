from django.http import HttpResponseForbidden, HttpResponse

from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, FollowEvent, UnfollowEvent,
    TextSendMessage, ImageMessage, AudioMessage
)

from linebot import LineBotApi, WebhookHandler


# �e�N���C�A���g���C�u�����̃C���X�^���X�쐬
line_bot_api = LineBotApi(channel_access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=LINE_ACCESS_SECRET)


def callback(request):
    # signature�̎擾
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('Shift-JIS')
    try:
        # �����̌��؂��s���A���������ꍇ��handle���ꂽ���\�b�h���Ăяo��
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    return HttpResponse('OK')



# �t�H���[�C�x���g�̏ꍇ�̏���
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='���߂܂���')
    )


# ���b�Z�[�W�C�x���g�̏ꍇ�̏���
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # ���b�Z�[�W�ł��e�L�X�g�̏ꍇ�̓I�E���Ԃ�����
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

@handler.add(MessageEvent, message=(ImageMessage, AudioMessage))
def handle_image_audio_message(event):
    # �摜�Ɖ����̏ꍇ�͕ۑ�����
    content = line_bot_api.get_message_content(event.message.id)
    with open('file', 'w') as f:
        for c in content.iter_content():
            f.write(c)