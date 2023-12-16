import os
import sys
import pkg_resources
import pyperclip
import requests
from tkinter import Tk, messagebox, Button, Label
from rich.console import Console
from tkinter import Tk, messagebox, Button, Label

class Protection:
    def __init__(self):
        self.console = Console()
        
    def get_board_number(self):
        try:
            command = "wmic baseboard get serialnumber"
            serial_number = os.popen(command).read().strip()
            # Removing the header "SerialNumber" from the output
            return serial_number.split('\n')[2].strip()
        except Exception as e:
            self.console.print(f"Error getting board number: {e}", style="bold red")
            return None

    def create_message_window(self,board_number):
        # إنشاء نافذة جديدة لـ tkinter
        message_window = Tk()
        message_window.title("رقم اللوحة غير موجود")
        
        # إضافة الرسالة إلى النافذة
        Label(message_window, text=f"رقم اللوحة الخاصة بك هو: {board_number}\nيرجى إرسال هذا الرقم إلى مطور البرنامج.").pack()

        # إضافة زر لنسخ رقم اللوحة إلى الحافظة
        Button(message_window, text="نسخ رقم اللوحة", command=lambda: self.copy_to_clipboard(message_window, board_number)).pack()

        # إظهار النافذة وبدء حلقة الحدث
        message_window.mainloop()

    def copy_to_clipboard(self,message_window, board_number):
        # نسخ رقم اللوحة إلى الحافظة
        message_window.clipboard_clear()
        message_window.clipboard_append(board_number)
        message_window.update_idletasks()
        Label(message_window, text="The plate number has been copied to the clipboard.").pack()

    def check_board_number(self):
        board_number = self.get_board_number()
        if not board_number:
            self.console.print("Plate number not found.", style="bold red")
            sys.exit(1)

        url = "https://back-end-api-python.vercel.app/auth/check"
        data = {"boardNumber": board_number}
        response = requests.post(url, json=data)
        response_data = response.json()

        if response_data.get("status"):
            self.console.print("The plate number is valid.", style="bold green")
        else:
            self.console.print("Plate number not found.", style="bold red")
            # إنشاء نافذة رسالة مع زر لنسخ رقم اللوحة
            self.create_message_window(board_number)
            sys.exit(1)
