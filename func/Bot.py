import os
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import random
from selenium.webdriver.support.ui import Select
from time import sleep
from func.EmailHandler import EmailHandler
from datetime import datetime
import shutil
driver_lock = threading.Lock()

class Bot:
    def __init__(self, profile_id, use_proxy,proxy,username):
        self.EmailHandler = EmailHandler()
        self.profile_id = profile_id
        self.proxy = proxy if use_proxy else None
        self.use_proxy = use_proxy
        self.username_proxy = "oyvmncvu"  # تأكد من وضع القيم الصحيحة هنا
        self.password_proxy = "drt3h8n35d7e"  # تأكد من وضع القيم الصحيحة هنا
        self.account = self.EmailHandler.get_information_account()
        self.username = username
        self.initialize_driver()  # تم نقل هذا السطر ليكون بعد تهيئة الخصائص
    
    def WaitElement(self, selector, selector_type):
        try:
            wait = WebDriverWait(self.driver, 10)
            return wait.until(EC.element_to_be_clickable((selector_type, selector)))
        except Exception as e:
            print(e)
            return None
    def next_up(self,target):
        try:           
            next_up_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, target)))  # استبدل بالمحدد الصحيح
            if next_up_button:
                next_up_button.click()
            else:
                print("Next button not found or not clickable")
        except Exception as e:
            print(f"Error in next_up: {e}")

    def signup(self):
        try:
            # استخدام WebDriverWait للانتظار حتى يصبح زر التسجيل قابلًا للنقر
            signup_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="signup-button"]')))
            signup_button.click()

            # ملء اسم المستخدم وكلمة المرور
            inputusername = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'signup-username')))
            inputusername.send_keys(self.username)

            inputpassword = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'password-input')))
            inputpassword.send_keys(self.account[0])

            # النقر على زر next up
            self.next_up('[data-a-target="segmented-signup-next-button"]')

            use_email = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="signup-phone-email-toggle"]')))
            use_email.click()

            inputemail = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'email-input')))
            inputemail.send_keys(self.account[1])
            self.next_up('[data-a-target="segmented-signup-next-button"]')
        
            current_year = datetime.now().year
            year_of_birth = random.randint(current_year - 25, current_year - 1)
            month_of_birth = random.choice(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
            day_of_birth = random.randint(1, 28)  # لضمان أن اليوم صالح لجميع الأشهر

            # اختيار الشهر من القائمة المنسدلة
            select_month = Select(WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="birthday-month-select"]'))))
            select_month.select_by_visible_text(month_of_birth)

            # إدخال اليوم في حقل النص داخل div
            input_day = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-a-target="birthday-date-input"] input')))
            input_day.clear()
            input_day.send_keys(str(day_of_birth))

            # إدخال السنة في حقل النص داخل div
            input_year = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-a-target="birthday-year-input"] input')))
            input_year.clear()
            input_year.send_keys(str(year_of_birth))
            self.next_up('[data-a-target="passport-signup-button"]')
            # التحقق من رسالة "This username is unavailable"
            # if WebDriverWait(self.driver, 3).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-live="polite"]'))):
            #     self.driver.quit()
            #     with open('src/data/bad_username.txt', 'a') as file:
            #         file.write(self.username + '\n')

        except Exception as e:
            print(f"Error in signup: {e}")

    def open_url(self, url):
        try:
            self.driver.get(url)
            self.signup()
        except Exception as e:
            print(f"Error in open_url: {e}")

    def create_proxy_auth_extension(self):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            }
        }
        """

        background_js = f"""
        var config = {{
                mode: "fixed_servers",
                rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{self.proxy.split(':')[0]}",
                    port: parseInt({self.proxy.split(':')[1]})
                }},
                bypassList: ["localhost"]
                }}
            }};

        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

        chrome.webRequest.onAuthRequired.addListener(
                function(details) {{
                    return {{
                        authCredentials: {{
                            username: "{self.username_proxy}",
                            password: "{self.password_proxy}"
                        }}
                    }};
                }},
                {{urls: ["<all_urls>"]}},
                ['blocking']
        );
        """

        # Updated directory path
        ext_dir = "C:\\Program Files\\Google\\Chrome\\Application\\119.0.6045.160\\src\\temp_proxy_extension_{}".format(self.profile_id)
        
        # Check and create directory with administrative privileges if necessary
        if not os.path.exists(ext_dir):
            try:
                os.makedirs(ext_dir, exist_ok=True)
            except PermissionError:
                raise PermissionError("Administrative privileges required to create directory at {}".format(ext_dir))

        manifest_path = os.path.join(ext_dir, 'manifest.json')
        with open(manifest_path, 'w') as f:
            f.write(manifest_json)

        background_path = os.path.join(ext_dir, 'background.js')
        with open(background_path, 'w') as f:
            f.write(background_js)
        return ext_dir
    
    def initialize_driver(self):
        global driver_lock
        with driver_lock:
            options = uc.ChromeOptions()
            # تمكين الامتدادات
            options.add_argument("--enable-extensions")
            options.add_argument("--allow-in-incognito")

            # إضافة امتدادات
            # باقي الكود ...
            if self.use_proxy and self.proxy:
                proxy_extension_dir = self.create_proxy_auth_extension()
                print(proxy_extension_dir)
                # Concatenate paths with a comma, no spaces
                extensions_path = f"{proxy_extension_dir}"

                # Use the concatenated paths in the load-extension argument
                options.add_argument(f"--load-extension={extensions_path}")
            profile_path = "C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\chromedriver\\{self.profile_id}"
            if os.path.exists(profile_path):
                    shutil.rmtree(profile_path)
            options.add_argument(f"--user-data-dir=C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\chromedriver\\{self.profile_id}")
            self.driver = uc.Chrome(options=options, use_subprocess=True)

    def start(self):
        print(self.proxy)
        try:
            url = "https://www.twitch.tv/"
            self.open_url(url)

            while True:  # حلقة لا نهائية لإبقاء السكريبت يعمل
                sleep(60)  # توقف لفترة قصيرة لتقليل استهلاك الموارد

        except Exception as e:
            print(f"An error occurred in start method: {e}")

