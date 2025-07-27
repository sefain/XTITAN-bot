# app.py
from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = '123abc_verify'
PAGE_ACCESS_TOKEN = 'ضع توكن صفحة فيسبوك هنا'

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'خطأ في التحقق', 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data['entry']:
        for event in entry['messaging']:
            sender = event['sender']['id']
            if 'message' in event:
                message_text = event['message']['text']
                send_message(sender, f'📩 لقد أرسلت: {message_text}')
    return 'OK', 200

def send_message(recipient_id, text):
    url = f'https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': text}
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run()
