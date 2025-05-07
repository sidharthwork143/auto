import os
import asyncio
import threading
from pyrogram import Client, filters, idle
from flask import Flask
from datetime import datetime
import random
import logging

# Environment Variables
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHAT = os.getenv("LOG_CHAT", "-1001728240047")  # Admin log chat ID
DELETE_TIME = int(os.getenv("DELETE_TIME", 5))  # Default delete time
PORT = int(os.getenv("PORT", 8080))  # Port for Flask server

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("⚠️ Missing essential API credentials in environment variables!")

app = Client("auto_delete_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
flask_app = Flask(__name__)

# Flask Health Check (for Koyeb)
@flask_app.route('/')
def home():
    return "✅ Bot Running Successfully!"

# Auto-delete message function
async def delete_message(chat_id, message_id, delay):
    await asyncio.sleep(delay * 60)
    await app.delete_messages(chat_id, message_id)

# Auto-delete normal messages
@app.on_message(filters.group & ~filters.service)
async def auto_delete(client, message):
    client.loop.create_task(delete_message(message.chat.id, message.message_id, DELETE_TIME))

# Command to adjust delete timer
@app.on_message(filters.command("set_autodelete", prefixes="/") & filters.group)
async def set_timer(client, message):
    global DELETE_TIME
    try:
        new_time = int(message.text.split()[1])
        DELETE_TIME = max(1, new_time)
        await message.reply(f"✅ Auto-delete time updated: {DELETE_TIME} minutes")
    except:
        await message.reply("❌ Use: `/set_autodelete <minutes>`")

# Auto-delete specific message types (images, links, keywords)
@app.on_message(filters.photo | filters.regex(r"https?://") | filters.text & filters.regex("delete_this"))
async def selective_delete(client, message):
    client.loop.create_task(delete_message(message.chat.id, message.message_id, DELETE_TIME))

# Logging deleted messages before removal
logging.basicConfig(level=logging.INFO)

@app.on_message(filters.group)
async def log_deleted_message(client, message):
    log_msg = f"🛑 Deleted message: {message.text} | From: {message.chat.id}"
    logging.info(log_msg)
    await app.send_message(LOG_CHAT, log_msg)

# Auto-Welcome New Group Members
@app.on_message(filters.new_chat_members)
async def welcome(client, message):
    for user in message.new_chat_members:
        await message.reply(f"👋 Welcome, {user.first_name}! Enjoy your stay!")

# Greeting based on time of day
@app.on_message(filters.text & filters.regex(r"(?i)hello|good morning|good night"))
async def auto_greet(client, message):
    hour = datetime.now().hour
    if hour < 12:
        response = "🌅 Good morning! Have a productive day ahead! 🚀"
    elif hour < 18:
        response = "☀️ Good afternoon! Hope your day is going well!"
    else:
        response = "🌙 Good night! Sweet dreams and rest well! 😴"
    await message.reply(response)

# AI-Based Smart Replies
funny_replies = [
    "😂 Are you serious?",
    "🤔 Hmm, interesting!",
    "🔥 That was a spicy message!",
    "🌟 Keep spreading positivity!"
]

@app.on_message(filters.text & filters.regex(r"(?i)how are you|what's up"))
async def random_reply(client, message):
    await message.reply(random.choice(funny_replies))

# Start command with static image & romantic shayari
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

# Bot & Flask Server Running Together
def run_flask():
    flask_app.run(host="0.0.0.0", port=PORT)

async def start_bot():
    await app.start()
    print("✅ Bot is running...")
    await idle()  # Keeps bot alive

threading.Thread(target=run_flask).start()
asyncio.run(start_bot())
