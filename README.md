
# Selenium Automation Bot

## Overview
This Python script utilizes Selenium with undetected_chromedriver to automate web interactions, specifically designed for creating accounts on a specific platform (e.g., Twitch). The script makes use of multi-threading, proxies, and Selenium's WebDriver to interact with web elements.

## Features
- **Proxy Support:** Ability to use proxies for web requests.
- **Email Handling:** Integrates an `EmailHandler` class for email interactions.
- **Automatic Form Filling:** Automates the process of filling out signup forms.
- **Custom Wait Conditions:** Waits for specific elements to become available or clickable, enhancing stability.
- **Date Selection:** Randomly selects a date of birth within a specified range.
- **Exception Handling:** Catches and logs exceptions for troubleshooting.

## Classes and Methods

### `class Bot`
- **__init__(self, profile_id, use_proxy, proxy, username):** Initializes the bot with user details and proxy settings.
- **WaitElement(self, selector, selector_type):** Waits for an element to be clickable based on the provided selector.
- **next_up(self, target):** Clicks the 'next up' button during the signup process.
- **signup(self):** Handles the entire signup process, including filling in user details and navigating through the signup steps.
- **open_url(self, url):** Opens a URL and starts the signup process.
- **create_proxy_auth_extension(self):** Creates a Chrome extension for proxy authentication.
- **initialize_driver(self):** Initializes the Chrome WebDriver with necessary options and extensions.
- **start(self):** Starts the bot and keeps it running in a loop.

## Setup and Execution
1. **Dependencies:** Ensure `selenium` and `undetected_chromedriver` are installed.
2. **Proxy Configuration:** If using a proxy, configure the proxy settings in the `__init__` method.
3. **Driver Path:** Set the path for ChromeDriver and user data directory.
4. **Execution:** Run the script. The bot will automate the web interaction based on the defined logic.

## Disclaimer
This script is for educational purposes only. Automated web interactions, especially account creation, can violate the terms of service of many websites.
