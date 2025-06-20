import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import CommandHandler, Updater
import logging

TOKEN = "7581412770:AAEljXoaA3O4vfVRwOnu0SZ822eElhWxzwM"
CHANNEL_ID = "@mlbblite12"

def get_latest_apk_info():
    url = "https://apkpure.com/mobile-legends-lite/com.mobile.legends.lite"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")

    title = soup.find("h1").text.strip()
    version = soup.select_one(".details-sdk span").text.strip() if soup.select_one(".details-sdk span") else "Unknown"
    download_link = soup.select_one("a.da").get("href")

    post_text = f"📢 **{title}** APK Update\n\n📌 Version: {version}\n📥 Download Link:\n➡️ https://apkpure.com{download_link}\n\n🇲🇲 Myanmar မှာ Play Store မရတဲ့အတွက် APK ကို ဒီနေရာကနေ Download လုပ်လို့ရပါတယ်။ VPN မလိုပါ။"
    return post_text

def check_update(update, context):
    try:
        bot = context.bot
        text = get_latest_apk_info()
        bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode='Markdown')
    except Exception as e:
        logging.error("Error posting update: %s", e)
        update.message.reply_text("❌ Update check failed.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("check_update", check_update))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
