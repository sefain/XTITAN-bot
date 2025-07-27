# app.py

import os
from flask import Flask, request
import requests

app = Flask(__name__)

# ✅ استدعاء المتغيرات من البيئة (Render Environment Variables)
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')

# ✅ هذا المسار يستخدمه فيسبوك للتحقق من التوكن عند ربط الـ Webhook
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'خطأ في التحقق', 403

# ✅ هذا هو الـ Webhook الذي يستقبل رسائل المستخدمين من فيسبوك
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data.get('entry', []):
        for event in entry.get('messaging', []):
            sender = event['sender']['id']
            if 'message' in event:
                message_text = event['message'].get('text', '')
                send_message(sender, f'📩 لقد أرسلت: {message_text}')
    return 'OK', 200

# ✅ دالة إرسال الرد إلى المستخدم
def send_message(recipient_id, text):
    url = f'https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': text}
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print('❌ خطأ في الإرسال:', response.text)

# ✅ تشغيل الخادم على الإنترنت (مثل Render)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
