import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from aiohttp import web

# --- Environment Variables ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Bot Setup ---
app = Client("auto_delete_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
delete_after = 300  # Default delete time: 5 minutes

# --- Dummy Web Server for Koyeb Health Check ---
async def handle(request):
    return web.Response(text="🤖 Bot is running on Koyeb!")

async def start_web_app():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=8080)
    await site.start()

# --- Bot Handlers ---
@app.on_message(filters.text & filters.group)  # Only group messages
async def delete_later(client, message: Message):
    print(f"Received message in group: {message.text}")  # Log message for debugging
    await asyncio.sleep(delete_after)  # Wait for 5 minutes (300 seconds)
    try:
        await message.delete()  # Delete message after 5 minutes
    except Exception as e:
        print(f"Error deleting message: {e}")

# --- Main function to run the bot and web server ---
async def main():
    await start_web_app()  # Start Koyeb health check server
    await app.start()  # Start the Pyrogram bot
    print("✅ Bot started.")
    await asyncio.Event().wait()  # Keep bot running

if __name__ == "__main__":
    asyncio.run(main())

