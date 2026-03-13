import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped # यह 1.0.0 वर्ज़न के लिए है
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

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
        await message.reply(f"OTP इस तरह भेजें: `/otp {phone} {code.phone_code_hash} 12345`")
    except Exception as e:
        await message.reply(f"Error: {e}")

@bot.on_message(filters.command("otp") & filters.private)
async def otp_cmd(client, message):
    data = message.text.split()
    phone, p_hash, otp = data[1], data[2], data[3]
    try:
        await user_bot.sign_in(phone, p_hash, otp)
        await message.reply("✅ लॉगिन सफल! अब /play [ID/Username] भेजें।")
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
        path = await m.download()
        try:
            await call_py.join_group_call(target, AudioPiped(path))
            await m.reply(f"🎶 प्ले हो रहा है!")
        except Exception as e:
            await m.reply(f"Error: {e}")

print("बोट स्टार्ट हो रहा है...")
bot.run()

