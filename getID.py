from flask import Flask, request, abort
import requests
import json

app = Flask(__name__)

# Line Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = 'Ccblv+Wk2I3rC9n+fHP2Hh1teiIjFUXHn09lxA/S+9gO2mlvPZlPyaJHlAK/PN+ARViX+XrHzVSonp5UC683yn7cDJm30MRCfOfWnSPQHOAxhWKbqwu7oubY0/KhhzjT+5M92qyXuSaVLPQXNRkrTwdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '16c782e7afc652932956b75b6dddd5e6'

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    print(f"Request body: {body}")

    event = json.loads(body)['events'][0]
    
    # 偵測加入群組的事件
    if event['type'] == 'join':
        group_id = event['source']['groupId']
        print(f"Group ID: {group_id}")

        # 可回傳訊息給群組
        send_line_message(group_id, "感謝邀請我進入群組！")

    return 'OK'

def send_line_message(group_id, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    data = {
        "to": group_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=data)
    print(response.status_code, response.text)

if __name__ == "__main__":
    app.run()
