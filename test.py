import requests
import random
import string
import re

# إنشاء بريد إلكتروني جديد بشكل عشوائي
def create_email():
    # توليد اسم المستخدم عشوائيًا
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email_address = f"{username}@wireconnected.com"

    url = "https://api.mail.tm/accounts"
    data = {
        "address": email_address,
        "password": "Reem123123@"
    }
    response = requests.post(url, json=data)
    return response.json(), email_address

# تسجيل الدخول والحصول على Token
def login(email_address):
    url = "https://api.mail.tm/token"
    data = {
        "address":email_address,
        "password": "Reem123123@"
    }
    response = requests.post(url, json=data)
    return response.json()['token']

# جلب الرسائل واستخراج الأرقام
def get_messages(token):
    url = "https://api.mail.tm/messages"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    messages = response.json()

    for message in messages.get('hydra:member', []):
        subject = message.get('subject', '')
        # استخراج أول 6 أرقام من الـ subject
        numbers = re.findall(r'\d+', subject)
        first_6_numbers = ''.join(numbers)[:6]
        print(f"Subject: {subject}")
        print(f"First 6 Numbers: {first_6_numbers}")

    return messages

# استخدام الوظائف
email_info, email_address = create_email()
print(email_address)
token = login(email_address)
print(token)
messages = get_messages(token)
