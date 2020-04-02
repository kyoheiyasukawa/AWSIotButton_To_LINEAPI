import os
import urllib.parse
import urllib.request
import json

def lambda_handler(event, context):
    
    LINE_TOKEN      = os.environ.get("LINE_TOKEN")
    LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"
    
    clicktype = event['deviceEvent']['buttonClicked']['clickType']
    
     
    if (clicktype == "SINGLE"):
        msg = "暇だから誰か電話して I am bored. Please call me😗"
    elif (clicktype == "DOUBLE"):
        msg = "野菜がとれたよ/ I harvested some veggies🥕"
    elif (clicktype == "LONG"):
        msg = "緊急事態。助けて！/Help me🚓 🚑 🚒"
    else:
        msg = "clickTypeを正常に取得できませんでした"
             
    method  = "POST"
    headers = {"Authorization": "Bearer ＜put your token from LINE＞"}
    payload = {"message": msg}
    
    
    payload = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
    urllib.request.urlopen(req)