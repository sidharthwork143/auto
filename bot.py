import time
import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")

# Verify essential API credentials
if not TOKEN or not LOG_CHANNEL_ID:
    raise ValueError("⚠️ Missing essential API credentials in environment variables!")

# Default delete time (300 sec = 5 minutes)
DELETE_TIME = 300

romantic_shayari = """💖 तुझे देख कर ही मैं खो जाता हूँ,
    तेरा नाम सुनते ही मुस्कुरा जाता हूँ...💖"""

def start(update: Update, context: CallbackContext):
    """Send start message with shayari & log activity"""
    user = update.effective_user
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"{romantic_shayari}\n\n🌟 Hey {user.first_name}, bot activated!"
    )
    context.bot.send_message(
        chat_id=LOG_CHANNEL_ID,
        text=f"🚀 Bot started by {user.first_name} ({user.id}) in group: {update.message.chat.title}"
    )

def delete_messages(update: Update, context: CallbackContext):
    """Delete messages after DELETE_TIME"""
    msg = update.message
    time.sleep(DELETE_TIME)
    context.bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)

def set_delete_time(update: Update, context: CallbackContext):
    """Dynamically adjust deletion time"""
    global DELETE_TIME
    try:
        new_time = int(context.args[0])
        DELETE_TIME = new_time
        update.message.reply_text(f"⌛ Message deletion time updated to {DELETE_TIME} seconds.")
    except ValueError:
        update.message.reply_text("❌ Invalid format! Use /settime <seconds>.")

def main():
    """Main function to run bot"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("settime", set_delete_time))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, delete_messages))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
