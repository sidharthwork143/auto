import asyncio
import os
from pyrogram import Client, filters

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHAT = os.getenv("LOG_CHAT", "-1001234567890")  # Admin log chat ID
DELETE_TIME = int(os.getenv("DELETE_TIME", 5))  # Default delete time in minutes

app = Client("auto_delete_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Auto-delete message function
async def delete_message(chat_id, message_id, delay):
    await asyncio.sleep(delay * 60)
    await app.delete_messages(chat_id, message_id)

# Auto-delete normal messages
@app.on_message(filters.group & ~filters.service)
async def auto_delete(client, message):
    asyncio.create_task(delete_message(message.chat.id, message.message_id, DELETE_TIME))

# Command to adjust auto-delete timer
@app.on_message(filters.command("set_autodelete", prefixes="/") & filters.group)
async def set_timer(client, message):
    global DELETE_TIME
    try:
        new_time = int(message.text.split()[1])
        DELETE_TIME = max(1, new_time)  # At least 1 minute
        await message.reply(f"✅ Auto-delete time updated: {DELETE_TIME} minutes")
    except:
        await message.reply("❌ Use: `/set_autodelete <minutes>`")

# Auto-delete specific message types (images, links, keywords)
@app.on_message(filters.photo | filters.regex(r"https?://") | filters.text & filters.regex("delete_this"))
async def selective_delete(client, message):
    asyncio.create_task(delete_message(message.chat.id, message.message_id, DELETE_TIME))

# Logging deleted messages before removal
@app.on_message(filters.group)
async def log_deleted_message(client, message):
    await app.send_message(LOG_CHAT, f"Deleted message: {message.text}")

# Greeting auto-replies for "Hello" or "Good morning"
@app.on_message(filters.text & filters.regex(r"(?i)hello|good morning"))
async def auto_reply(client, message):
    await message.reply("🌟 Hello! Hope you have an amazing day! 😊")

# Start command with a static animal image and romantic shayari
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_photo(
        photo="https://vault.pictures/p/ff7a7f5d976e4f4289e961a9b90d78d8",  # Replace with direct image link
        caption="🌹 *Tumhe chahna meri aadat ban chuki hai...*\n\n_Kabhi sochta hoon, chand se keh doon tumse milne ka tareeka!_ 💖"
    )

# Interactive menu
@app.on_message(filters.command("menu") & filters.private)
async def menu(client, message):
    await message.reply_text(
        "🛠 **Bot Menu** 🛠\n\n- `/set_autodelete <minutes>` Adjust delete timer\n- `/start` Send welcome message\n- `/menu` Show options",
    )

app.run()
