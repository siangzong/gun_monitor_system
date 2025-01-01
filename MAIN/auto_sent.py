from linebot import LineBotApi
from linebot.models import TextSendMessage
from Lineapp.func import *
import requests
from linebot.models import MessageEvent, TextSendMessage
from linebot import LineBotApi

LINE_CHANNEL_ACCESS_TOKEN = 'E2itbmLLuMxOf1hSRf+zwuDUbsUYToMoBhEM2nxQH7zBcjbHOq/udV0br7wYpgLLSWGPuwUfjahHd2R9SkeQXqjNn9pVH4DnwKUmDKnSU4o/OxY16aS4KY127x8u52BNzMYgMwPYZe6hi2KyamOdiwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
def alert(raws):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    for raw in raws:

        raw = list(raw)

        if raw[5] is None:
            raw[5] = ''

        fortext = f"級職:{raw[1]}，姓名:{raw[2]}，鑰匙櫃狀態:{raw[4]}，時間:{raw[5]}"

        ids = find_line_id()
        for id in ids:
            try:
                line_bot_api.push_message(id, TextSendMessage(text=fortext))
            except Exception as e:
                print(f"無法發送訊息: {e}")

def alert_text(text):
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

    ids = find_line_id()
    for id in ids:
        try:
            line_bot_api.push_message(id, TextSendMessage(text=text))
        except Exception as e:
            print(f"無法發送訊息: {e}")