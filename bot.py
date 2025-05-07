import asyncio
from pyrogram import Client, filters
from datetime import datetime, timedelta

# Bot ke settings
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Default delete time (minutes)
DELETE_TIME = 5

app = Client("auto_delete_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Message delete function
async def delete_message(chat_id, message_id, delay):
    await asyncio.sleep(delay * 60)
    await app.delete_messages(chat_id, message_id)

# Auto-delete messages
@app.on_message(filters.group & ~filters.service)
async def auto_delete(client, message):
    asyncio.create_task(delete_message(message.chat.id, message.message_id, DELETE_TIME))

# Command to update delete time
@app.on_message(filters.command("set_timer", prefixes="/") & filters.group)
async def set_timer(client, message):
    global DELETE_TIME
    try:
        new_time = int(message.text.split()[1])
        DELETE_TIME = max(1, new_time)  # At least 1 minute
        await message.reply(f"✅ Auto-delete time updated: {DELETE_TIME} minutes")
    except:
        await message.reply("❌ Invalid command format!\nUse: `/set_timer <minutes>`")

# Start command - Show animal image and shayari
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_photo(
        photo="https://source.unsplash.com/400x400/?animal",
        caption="🌹 *Meri mohabbat ka silsila aaj bhi waisa hi hai...*\n\n_Chaand bhale hi badal jaye, magar tumse pyaar kabhi kam na hoga!_ 💖"
    )

app.run()
