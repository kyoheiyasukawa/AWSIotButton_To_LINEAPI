# AWSiotButtonToLineAPI
AWSIotButton(Click) →AWSLambda(Python&amp;Json)→LINE API →Message to your personal LINE account




#<b>経緯</b>
コロナの影響でおばあちゃんが家を出れずに退屈しているらしいのだが、
高齢のためライン（スマホ）が使えない。
孫１５人のラインに一斉送信して、おばあちゃんの相手をしてくれる人を探す！という公算。
たまたまAWSIotエンタープライズ(2500円)という面白いデバイスを発見したので、さっそく実装してみた。
![IMG_20200328_130139.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/609733/332bb675-f976-33a7-a59e-98fca8d712f9.jpeg)

アーチテクチャーはこんな感じです。
![ZZZ.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/609733/405097f4-744d-a09b-93ba-71e4d093593b.png)


#<b>手順</b>
#<b>①IOTボタンの設定</b>
AWS IoT 1-Click アプリをアップルストア又は、GooglePlayから自分のスマホにインストールし、デバイスの登録設定、Wifi設定を行ってください。

#<b>②LINE Notify のトークンを発行する</b>
トークンは、マイページの「アクセストークンの発行(開発者向け)」以下の「トークンを発行する」ボタンから発行できます。
[https://notify-bot.line.me]
トークン発行後、設定したルームに LINE notify を招待します。
#<b>③コマンドラインからトークンをPOSTする</b>
リナックスからはカールコマンドでPOSTします。
Windowsの場合 curl コマンドをダウンロードしてインストールしてください。[https://notify-bot.line.me]

```curl -X POST -H "Authorization: Bearer ＜取得したトークン＞" -F "message=test from curl" https://notify-api.line.me/api/notify```




カールコマンドからLINE Notifyにポストして自分のラインに"hello"とメッセージを送るテストをしてみてください。
 ```curl https://notify-api.linuthorization: Bearer ＜取得したトーケン＞' -F 'message=hello'```

#<b>④AWSLambdaを作成</b>
今回はPython3.8で実装してみました。

```
import os
import urllib.parse
import urllib.request
import json

def lambda_handler(event, context):
    
    LINE_TOKEN      = os.environ.get("LINE_TOKEN")
    LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"

    //クリックタイプをイベント情報として取得する
    clicktype = event['deviceEvent']['buttonClicked']['clickType']
    
    //クリックタイプに応じた処理の分岐
    if (clicktype == "SINGLE"):
        msg = "暇だから誰か電話して I am bored. Please call me😗"
    elif (clicktype == "DOUBLE"):
        msg = "野菜がとれたよ/ I harvested some veggies🥕"
    elif (clicktype == "LONG"):
        msg = "緊急事態。助けて！/Help me🚓 🚑 🚒"
    else:
        msg = "clickTypeを正常に取得できませんでした"
             
    method  = "POST"
    headers = {"Authorization": "Bearer ＜トークンをいれる＞"}
    payload = {"message": msg}
    
    
    payload = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
    urllib.request.urlopen(req)
```
#<b>④IotボタンとAWSLambdaを紐付ける</b>
AWSのAWS IoT 1-Clickのページに行き、
管理 > プロジェクト>作成ボタン
アクションから”Lambda関数を選択”を選ぶ。
Lambda関数のところを自分の作ったLambdaファイルを選択し、プロジェクトの作成をクリック。
#<b>④ボタンを押して見る　ポチッ</b>
ボタンを押せばAWSLambdaがキックされラインにメッセージが送られる!
![Screenshot_20200328_153549.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/609733/977013e7-8953-d912-6c2f-be611252f695.jpeg)

AWSLambdaを使えばサーバーレスで出来ちゃうんです。ラインだけではなくスマート家電、他のSNS等へのプッシュなどボタンの使い道は多様です。結構簡単に作れちゃうので是非試してみてください。

![IMG_20200328_154354.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/609733/44dcf6b1-0d84-dffb-25b7-81e621880e3b.png)

*最後までお読み頂きありがとうございました。*
