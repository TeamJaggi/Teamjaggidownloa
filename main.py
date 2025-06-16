import os
from telegram.ext import Updater, MessageHandler, Filters
from keep_alive import keep_alive
import requests
import re

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def get_download_link(url):
    try:
        api_url = f"https://save-from.net/api/convert?url={url}&lang=en"
        response = requests.get(api_url)
        data = response.json()
        if 'url' in data and 'url' in data['url']:
            return data['url']['url']
    except Exception as e:
        print("Error:", e)
    return None

def handle_message(update, context):
    text = update.message.text
    urls = re.findall(r'(https?://[^\s]+)', text)
    for url in urls:
        update.message.reply_text("🔍 Processing your link...")
        dl = get_download_link(url)
        if dl:
            update.message.reply_text(f"✅ Download Link:\n{dl}")
        else:
            update.message.reply_text("❌ Sorry, download link not found.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

keep_alive()
main()
