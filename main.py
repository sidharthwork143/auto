import logging
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import asyncio
import os

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Adult quote
ADULT_QUOTE = "Sex is like math: Add the bed, subtract the clothes, divide the legs, and hope you don't multiply. 🔥"

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ADULT_QUOTE)

# Message delete handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    # Only delete messages in groups
    if msg.chat.type in ["group", "supergroup"]:
        await asyncio.sleep(300)  # wait for 5 minutes
        try:
            await context.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        except Exception as e:
            logging.warning(f"Failed to delete message: {e}")

# Main function to run the bot
async def main():
    TOKEN = os.getenv("7847633442:AAHKWU_NDSvmndZ9QmtcYVekEsr_ZlYtcTE")  # use environment variable or replace below
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
