from func.Bot import Bot
from func.protection import Protection
from rich.console import Console
import platform
from threading import Thread
import threading
import keyboard
import sys

# تحديد المكتبات المطلوبة
REQUIRED_LIBS = ["selenium", "rich"]
console = Console()

def print_system_info():
    info = {
        "OS": platform.system(),
        "OS version": platform.release(),
        "Python version": platform.python_version(),
        "System Architecture": platform.machine(),
        "Script version": "First Edition Version",
    }

    console.print("[bold magenta]معلومات النظام:[/bold magenta]")
    for key, value in info.items():
        console.print(f"{key}: [bold cyan]{value}[/bold cyan]")

def load_proxies():
    with open("data/Proxy.txt", "r") as file:
        return [line.strip() for line in file]

def load_username():
    with open("data/username.txt", "r") as file:
        return [line.strip() for line in file]
      
def run_bot(profile_id,use_proxy, proxy,username):
    if use_proxy and proxy:
        bot = Bot(profile_id, use_proxy, proxy,username)
        bot.start()
    else:
        print("No more proxies available or use_proxy is False.")

# دالة لجلب رقم اللوحة
def hotkey_listener():
        # الاستماع لمجموعة المفاتيح Shift + Ctrl
        keyboard.add_hotkey('ctrl+q', lambda: sys.exit(1))
        keyboard.wait()
def main():
    threading.Thread(target=hotkey_listener, daemon=True).start()
    Protection().check_board_number()  # إضافة هذا السطر للتحقق من رقم اللوحة

    print("Main Menu:")
    print("1. Start Bots")
    print("2. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        num_pages = int(input("Enter number of pages to open (Max 25): "))
        num_pages = min(num_pages, 25)  # تأكيد أن العدد لا يتجاوز 25
        proxies = load_proxies()
        username = load_username()

        threads = []  # قائمة لحفظ الخيوط
        for i in range(num_pages):
            profile_id = f"Profile_{i+1}"
            proxy = proxies[i % len(proxies)]  # تكرار استخدام البروكسيات إذا لزم الأمر
            bot_thread = Thread(target=run_bot, args=(profile_id, True, proxy,username))
            bot_thread.start()  # بدء تشغيل الخيط
            threads.append(bot_thread)  # إضافة الخيط إلى القائمة

        for thread in threads:
            thread.join()  # انتظار انتهاء جميع الخيوط

    elif choice == "2":
        print("Exiting the program. Goodbye!")
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print_system_info()
    main()
