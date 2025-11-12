==============================
 WhatsApp Bot - Installation Guide
==============================

Thank you for using our WhatsApp automation system.
Below are the steps to run your bot:

1) Install Python from:
   https://www.python.org/downloads/

2) Open Command Prompt and install requirements:
   pip install -r requirements.txt

3) Start the bot:
   python app.py

4) Open ngrok (provided by developer):
   ngrok http 5000

5) Copy the HTTPS link provided by ngrok and add it to:
   WHEN A MESSAGE COMES IN (Twilio)
   Example:
   https://your-link.ngrok-free.app/webhook

6) Your bot is now live ✅
Any message sent to your WhatsApp API number will reach the bot.

Configuration:
--------------
Edit "config.json" to change:
- Bot responses
- Welcome messages
- Keywords

Logs:
------
All messages are recorded inside:
logs/messages.log

Support:
--------
Contact your developer for any modifications.