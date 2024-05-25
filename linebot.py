import os
from linebot import LineBotApi
from linebot.models import (
    QuickReplyButton, MessageAction, QuickReply, TextSendMessage, ImageSendMessage
)

line_bot_api = LineBotApi(
    os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
)

# linebot
"""
> メッセージ送信
send_message( reply_token, text )
    reply_token -> string
    text -> string or list( in string )

> クイックリプライ送信
quick_reply( reply_token, text, action_label, action_text )
    reply_token -> string
    text -> string
    ( action_label, action_text  ) -> string or list( in string )

"""


def send_message(reply_token, text):

    # make TextMessage
    message_object = []
    if isinstance(text, str):
        message_object.append(TextSendMessage(text=text))
    elif isinstance(text, list):
        for tex_nest in text:
            message_object.append(TextSendMessage(text=tex_nest))
    else:
        return "TextMessage Value Error, please input list or string"

    # SendMessage
    line_bot_api.reply_message(
        reply_token,
        message_object
    )
    return


def quick_reply(reply_token, text, action_label, action_text, image_path=None):

    # Create quickreply botton
    items = []
    if isinstance(action_label, str) and isinstance(action_text, str):
        items.append(QuickReplyButton(
            action=MessageAction(
                label=action_label,
                text=action_text
            )
        )
        )
    else:
        for (label_ele, action_ele) in zip(action_label, action_text):
            items.append(QuickReplyButton(
                action=MessageAction(
                    label=label_ele,
                    text=action_ele
                )
            )
            )

    text_message = TextSendMessage(
        text=text,
        quick_reply=QuickReply(items=items)
    )

    if image_path:
        image_message = ImageSendMessage(
            original_content_url=image_path,
            preview_image_url=image_path
        )
        # テキストメッセージと画像メッセージを同時に送信
        line_bot_api.reply_message(
            reply_token,
            messages=[image_message, text_message]
        )
    else:
        # テキストメッセージのみ送信
        line_bot_api.reply_message(
            reply_token,
            messages=[text_message]
        )

    return
