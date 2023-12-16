import requests
import random
import string
import time
import re
import secrets
from threading import Thread

class EmailHandler:
    def __init__(self):
        # Initialize instance variables
        self.email_address = None
        self.password = "Reem123123@"  # Default password, can be changed as needed
        self.account_info = None
        self.token = None
        self.generate_password()  # Generate a new password
        self.create_email()       # Create a new email account
    def get_information_account(self):
        return [self.password , self.email_address]
    def generate_password(self, length=12):
        # Generate a secure password of specified length
        password = secrets.token_hex(length // 2)
        self.password = f"{password[:length]}"

    def create_email(self):
        # Generate a random username for the email address
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.email_address = f"{username}@wireconnected.com"

        # Create the email account using Mail.tm API
        url = "https://api.mail.tm/accounts"
        data = {"address": self.email_address, "password": self.password}
        response = requests.post(url, json=data)
        self.account_info = response.json()  # Store account information
        return self.account_info, self.email_address

    def login(self):
        # Login to the email account using Mail.tm API
        url = "https://api.mail.tm/token"
        data = {"address": self.email_address, "password": self.password}
        response = requests.post(url, json=data)

        # Check response and extract token
        if response.status_code == 200 and 'token' in response.json():
            self.token = response.json()['token']
            return self.token
        else:
            # Print error response if login fails
            print("Error in login:", response.text)
            return None

    def get_messages(self):
        # Fetch messages from the email account
        url = "https://api.mail.tm/messages"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        messages = response.json()

        for message in messages.get('hydra:member', []):
            subject = message.get('subject', '')
            # Extract and print the first 6 numbers from each subject
            numbers = re.findall(r'\d+', subject)
            first_6_numbers = ''.join(numbers)[:6]
            print(f"Subject: {subject}")
            print(f"First 6 Numbers: {first_6_numbers}")

        return messages

    def get_verification_code(self):
        # Attempt to login and retrieve messages
        self.login()
        messages = self.get_messages()

        # Extract and return the verification code from email subjects
        for message in messages.get('hydra:member', []):
            subject = message.get('subject', '')
            numbers = re.findall(r'\d+', subject)
            first_6_numbers = ''.join(numbers)[:6]
            if first_6_numbers:
                return first_6_numbers
        return None

    def check_verification_code(self):
        # Continuously check for verification code every 10 seconds
        while True:
            verification_code = self.get_verification_code()
            if verification_code:
                print(f"Verification Code: {verification_code}")
                return verification_code
            time.sleep(10)  # Delay before next check

    def start_verification_check(self):
        # Start the verification check in a separate thread
        print(self.email_address)
        print(self.password)
        Thread(target=self.check_verification_code).start()

# Create an instance of EmailHandler and start the verification check
# bot = EmailHandler()
# bot.start_verification_check()
