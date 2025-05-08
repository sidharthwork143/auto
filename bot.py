from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os
from aiohttp import web
import threading

# --- HTTP Server for Koyeb health check ---
async def handle(request):
    return web.Response(text="🤖 Bot is running on Koyeb!")

def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=8080)

# --- Environment Variables ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Bot Config ---
delete_after = {}  # Stores custom delete time per chat
app = Client("auto_delete_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

ROMANTIC_SHAYARI = """💌
*Ek pal ki mohabbat mein zindagi badal gayi,*
*Tera dekha to meri duniya badal gayi.*
*Tujh se milkar aisa laga mujhe,*
*Jaise barson ki pyaas mein barsaat mil gayi...*
"""

# --- Bot Handlers ---
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(ROMANTIC_SHAYARI, quote=True)

@app.on_message(filters.command("settime") & filters.group)
async def set_time(client, message: Message):
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat_id = message.chat.id

    member = await client.get_chat_member(chat_id, user_id)
    if member.status not in ("administrator", "creator"):
        await message.reply("⛔ Sirf admin hi timer set kar sakte hain.")
        return

    try:
        seconds = int(message.text.split(maxsplit=1)[1])
        if seconds < 10 or seconds > 86400:
            await message.reply("⚠️ Time 10 se 86400 seconds (1 day) ke beech hona chahiye.")
            return
        delete_after[chat_id] = seconds
        await message.reply(f"✅ Messages ab {seconds} seconds baad delete honge.")
    except:
        await message.reply("❌ Galat format. Use: `/settime 300`", quote=True)

@app.on_message(filters.command("gettime") & filters.group)
async def get_time(client, message: Message):
    chat_id = message.chat.id
    seconds = delete_after.get(chat_id, 300)
    await message.reply(f"🕒 Current auto-delete time: {seconds} seconds.")

@app.on_message(filters.text & ~filters.command(["start", "settime", "gettime"]) & filters.group)
async def delete_later(client, message: Message):
    chat_id = message.chat.id
    time_to_delete = delete_after.get(chat_id, 300)  # Default 5 mins
    await asyncio.sleep(time_to_delete)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")

# --- Start the bot and web server ---
if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    app.run()
