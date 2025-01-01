from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import os 
from Lineapp.func import *
from auto_sent import *


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_ACCESS_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        

        for event in events:


            user_id = event.source.user_id
            profile = line_bot_api.get_profile(user_id)
            check=check_line_user(profile.display_name)
            if check==0:
                store_line_user(user_id,profile.display_name)


            if isinstance(event, MessageEvent):
                mtext = event.message.text

                if mtext == "help" or mtext == "HELP":
                    try:
                        message = TextSendMessage(text="查看目前鑰匙櫃的狀態：鑰匙櫃狀態\n查看目前槍枝是否領用狀態：槍櫃狀態\n查看今日武館室進出紀錄(50筆)：人員進出紀錄\n查看今日鑰匙櫃開關紀錄(10筆)：鑰匙櫃紀錄\n查看今日武器進出紀錄(50筆)：武器進出紀錄")
                        line_bot_api.reply_message(event.reply_token, message)
                    except LineBotApiError as e:
                        return HttpResponseBadRequest(f"LINE API error: {str(e)}")
                
                elif mtext == "鑰匙櫃狀態":
                    rows=cabinet_state_search()
                    if rows:
                        for row in rows:
                            data=f"目前狀態：開啟\n級職:{row[1]},姓名:{row[2]},時間:{row[5]}"
                        message = TextSendMessage(text=data)
                        line_bot_api.reply_message(event.reply_token, message)
                    else:
                        message = TextSendMessage(text="目前狀態：關閉\n無人開啟")
                        line_bot_api.reply_message(event.reply_token, message)

                elif mtext == "槍櫃狀態":
                    rows=gun_state_search()
                    data=""
                    if rows:
                        for row in rows:
                            data+=f"槍枝序號:{row[1]},姓名:{row[2]},時間:{row[4]}\n"
                        message = TextSendMessage(text=data.strip())
                        line_bot_api.reply_message(event.reply_token, message)
                    else:
                        message = TextSendMessage(text="無槍取出")
                        line_bot_api.reply_message(event.reply_token, message)
                
                elif mtext == "人員進出紀錄":
                    try:
                        ans=read_log(50,'entry_and_exit')
                        if ans==0:ans="無紀錄"
                        message = TextSendMessage(text=ans)
                        line_bot_api.reply_message(event.reply_token, message)
                        
                    except LineBotApiError as e:
                        return HttpResponseBadRequest(f"LINE API error: {str(e)}")
                    
                elif mtext == "鑰匙櫃紀錄":
                    try:
                        ans=read_log(10,'cabinet')
                        if ans==0:ans="無紀錄"
                        message = TextSendMessage(text=ans)
                        line_bot_api.reply_message(event.reply_token, message)
                        
                    except LineBotApiError as e:
                        return HttpResponseBadRequest(f"LINE API error: {str(e)}")
                elif mtext == "武器進出紀錄":
                    try:
                        ans=read_log(50,'gun_state')
                        if ans==0:ans="無紀錄"
                        message = TextSendMessage(text=ans)
                        line_bot_api.reply_message(event.reply_token, message)
                        
                    except LineBotApiError as e:
                        return HttpResponseBadRequest(f"LINE API error: {str(e)}")




        return HttpResponse()  
    else:
        return HttpResponseBadRequest()  


