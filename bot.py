from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Default delete time in seconds (5 minutes)
delete_after = {}

app = Client("autodelete_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


ROMANTIC_SHAYARI = """💌
*Ek pal ki mohabbat mein zindagi badal gayi,*
*Tera dekha to meri duniya badal gayi.*
*Tujh se milkar aisa laga mujhe,*
*Jaise barson ki pyaas mein barsaat mil gayi...*
"""

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(ROMANTIC_SHAYARI, quote=True)

@app.on_message(filters.command("settime") & filters.group)
async def set_time(client, message: Message):
    global delete_after
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
        delete_after[chat_id] = seconds
        await message.reply(f"✅ Messages ab {seconds} seconds baad delete honge.")
    except:
        await message.reply("❌ Galat format. Use: `/settime 300`", quote=True)

@app.on_message(filters.text & ~filters.command(["start", "settime"]))
async def delete_later(client, message: Message):
    chat_id = message.chat.id
    time_to_delete = delete_after.get(chat_id, 300)  # Default 300 sec
    await asyncio.sleep(time_to_delete)
    try:
        await message.delete()
    except:
        pass

if __name__ == "__main__":
    app.run()
