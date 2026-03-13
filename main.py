import asyncio
import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

# बोट और क्लाइंट सेटअप
bot = Client("MasterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_bot = Client("user_session", api_id=API_ID, api_hash=API_HASH)
call_py = PyTgCalls(user_bot)

SUDO_USERS = {OWNER_ID}

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if message.from_user.id not in SUDO_USERS:
        return await message.reply("🔒 एक्सेस डिनाइड!")
    await message.reply("नमस्ते! /login [नंबर] से लॉगिन करें।")

@bot.on_message(filters.command("approve") & filters.user(OWNER_ID))
async def approve(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user = await client.get_users(message.command[1])
        user_id = user.id
    else: return
    SUDO_USERS.add(user_id)
    await message.reply(f"✅ User {user_id} ऑथराइज्ड है।")

@bot.on_message(filters.command("login") & filters.private)
async def login_cmd(client, message):
    if message.from_user.id not in SUDO_USERS: return
    phone = message.text.split()[1]
    await user_bot.connect()
    try:
        code = await user_bot.send_code(phone)
        await message.reply(f"OTP कोड प्राप्त होने पर इस तरह भेजें:\n`/otp {phone} [HASH] 12345`")
        # नोट: यहाँ hash को ट्रैक करने के लिए कोड है
        global phone_hash
        phone_hash = code.phone_code_hash
    except Exception as e:
        await message.reply(f"Error: {e}")

@bot.on_message(filters.command("otp") & filters.private)
async def otp_cmd(client, message):
    data = message.text.split()
    phone, otp = data[1], data[2]
    try:
        await user_bot.sign_in(phone, phone_hash, otp)
        await message.reply("✅ लॉगिन सफल! अब /play [ID] का उपयोग करें।")
        if not call_py.active:
            await call_py.start()
    except Exception as e:
        await message.reply(f"Error: {e}")

@bot.on_message(filters.command("play") & filters.private)
async def play_voice(client, message):
    if message.from_user.id not in SUDO_USERS: return
    target = message.text.split(None, 1)[1]
    await message.reply(f"अब {target} के लिए वॉइस मैसेज भेजें।")

    @bot.on_message(filters.voice & filters.private)
    async def stream(c, m):
        msg = await m.reply("प्रक्रिया जारी है...")
        path = await m.download()
        try:
            await call_py.join_group_call(target, AudioPiped(path))
            await msg.edit(f"🎶 प्ले हो रहा है!")
        except Exception as e:
            await msg.edit(f"Error: {e}")

bot.run()

