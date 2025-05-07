import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")

if not TOKEN or not LOG_CHANNEL_ID:
    raise ValueError("⚠️ Missing essential API credentials in environment variables!")

DELETE_TIME = 300  # Default delete time (300 sec = 5 minutes)

romantic_shayari = """💖 तुझे देख कर ही मैं खो जाता हूँ,
    तेरा नाम सुनते ही मुस्कुरा जाता हूँ...💖"""

async def start(update: Update, context):
    """Send start message with shayari & log activity"""
    user = update.effective_user
    await update.message.reply_text(f"{romantic_shayari}\n\n🌟 Hey {user.first_name}, bot activated!")
    await context.bot.send_message(
        chat_id=LOG_CHANNEL_ID,
        text=f"🚀 Bot started by {user.first_name} ({user.id}) in group: {update.message.chat.title}"
    )

async def delete_messages(update: Update, context):
    """Delete messages after DELETE_TIME"""
    await asyncio.sleep(DELETE_TIME)
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

async def set_delete_time(update: Update, context):
    """Adjust deletion time"""
    global DELETE_TIME
    try:
        new_time = int(update.message.text.split()[1])
        DELETE_TIME = new_time
        await update.message.reply_text(f"⌛ Message deletion time updated to {DELETE_TIME} seconds.")
    except ValueError:
        await update.message.reply_text("❌ Invalid format! Use /settime <seconds>.")

async def main():
    """Run bot with proper event loop cleanup"""
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("settime", set_delete_time))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_messages))

    print("🚀 Bot is running...")
    
    try:
        await app.run_polling()
    except KeyboardInterrupt:
        print("⛔ Bot shutting down...")
    finally:
        await app.shutdown()

# Fix: Properly close event loop to avoid RuntimeError
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()
