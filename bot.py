import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from aiohttp import web

# --- ENV VARIABLES ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Setup bot client ---
app = Client("koyeb_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Web server for Koyeb health check ---
async def web_handler(request):
    return web.Response(text="✅ Bot is alive!")

async def run_web():
    app_web = web.Application()
    app_web.router.add_get("/", web_handler)
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

# --- /start command ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text(
        "**🤣 Adult Joke 🤭**\n\n"
        "*Biwi ne kaha: Jab bhi tum mujhe dekho, kuch karne ka mann nahi karta.*\n"
        "*Pati bola: Tumhara kaam ho gaya, mera mood kharaab karne ka...*"
    )

# --- Auto-delete group messages ---
@app.on_message(filters.group & filters.text)
async def auto_delete(client, message: Message):
    await asyncio.sleep(300)  # 5 minutes = 300 seconds
    try:
        await message.delete()
    except Exception as e:
        print(f"Delete error: {e}")

# --- Main run block ---
async def main():
    await run_web()       # start web server for Koyeb health check
    await app.start()     # start Telegram bot
    print("🤖 Bot is running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
