from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

# টোকেন সেটআপ
BOT_TOKEN = "7968874233:AAFfkYyxZzu0iDLJ_acanYMwOEYVAL-Zqgg"
CHANNEL_ID = "@mede_max"

# চ্যানেল চেক ফাংশন
def check_subscription(user_id):
    # এখানে Telegram API কল করে চ্যানেল মেম্বারশিপ যাচাই করুন
    return True  # উদাহরণস্বরূপ

# /start কমান্ড
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    if check_subscription(user.id):
        update.message.reply_text("লিংক পাঠান ভিডিও ডাউনলোড করতে।")
    else:
        update.message.reply_text(f"আমাদের চ্যানেলে যোগ দিন: {CHANNEL_ID}")

# ভিডিও ডাউনলোড হ্যান্ডলার
def download_video(update: Update, context: CallbackContext):
    user = update.effective_user
    if not check_subscription(user.id):
        update.message.reply_text(f"চ্যানেলে যোগ দিন: {CHANNEL_ID}")
        return

    url = update.message.text
    update.message.reply_text("ভিডিও ডাউনলোড শুরু হচ্ছে...")
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        # ভিডিও টেলিগ্রামে পাঠান
        with open(file_name, 'rb') as video:
            context.bot.send_video(chat_id=update.effective_chat.id, video=video)

        # ডাউনলোড ফাইল মুছে ফেলুন
        os.remove(file_name)

    except Exception as e:
        update.message.reply_text("ডাউনলোডে সমস্যা হয়েছে।")
        print(e)

# বট রান
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()