# app.py

from flask import Flask, request
import requests

app = Flask(__name__)

# ⚙️ استخدم توكن التحقق نفسه الذي ستضعه في Meta Developer Console
VERIFY_TOKEN = 'my_secure_token'

# ✅ ضع هنا توكن الصفحة الحقيقي الذي حصلت عليه من Graph API
PAGE_ACCESS_TOKEN = 'EAAr4ed2A8oQBPJ82tGy1c6SIOwOZAzOt7qXYObIHbiEjZCa09ipd9Nt67i9ZA2L7wxjuK5Vj9MNZAgYgJDhLFjfpcltgzdYJieQ2ZA9DmNUyYobjyUvHhLEEA9CgtTgn4PT39X42IzOyZCaYZBETLfjZBVK8KRfLZCnRQat5iXXN2j8Upm73N610tp7M71uwLzcwmnZAy2EDZBymaK9imfUZCty9ApMqmZAZBTv18jZCLZAcZCtrANGU7KORBJyyLVhkIojCF'

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

# ✅ تشغيل الخادم محليًا أو على الإنترنت (Render / Replit / Glitch)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
