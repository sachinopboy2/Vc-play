import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

# बोट क्लाइंट
bot = Client("MasterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# यूजरबोट क्लाइंट (लॉगिन के लिए)
user_bot = None
call_py = None
SUDO_USERS = {OWNER_ID}

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if message.from_user.id not in SUDO_USERS:
        return await message.reply("🔒 आप ऑथराइज्ड नहीं हैं।")
    await message.reply("नमस्ते! /login [नंबर] से लॉगिन करें या /approve @username से किसी को परमिशन दें।")

# --- अप्रूवल सिस्टम ---
@bot.on_message(filters.command("approve") & filters.user(OWNER_ID))
async def approve(client, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user = await client.get_users(message.command[1])
        user_id = user.id
    else: return
    SUDO_USERS.add(user_id)
    await message.reply(f"✅ User {user_id} को अनुमति मिल गई।")

# --- लॉगिन सिस्टम ---
@bot.on_message(filters.command("login") & filters.private)
async def login(client, message):
    if message.from_user.id not in SUDO_USERS: return
    phone = message.text.split()[1]
    global user_bot
    user_bot = Client("user_session", api_id=API_ID, api_hash=API_HASH)
    await user_bot.connect()
    try:
        code_info = await user_bot.send_code(phone)
        await message.reply("📩 OTP भेज दिया गया है। अपना OTP इस तरह भेजें: `/otp 12345`")
        
        @bot.on_message(filters.command("otp") & filters.private)
        async def otp_cmd(c, m):
            otp = m.text.split()[1]
            await user_bot.sign_in(phone, code_info.phone_code_hash, otp)
            await m.reply("✅ लॉगिन सफल! अब आप /play [ID/Link] भेज सकते हैं।")
    except Exception as e:
        await message.reply(f"Error: {e}")

# --- VC प्ले सिस्टम ---
@bot.on_message(filters.command("play") & filters.private)
async def play(client, message):
    if message.from_user.id not in SUDO_USERS or not user_bot:
        return await message.reply("❌ पहले लॉगिन करें!")
    
    target_chat = message.text.split(None, 1)[1]
    await message.reply(f"ठीक है! अब वह **Voice Message** भेजें जिसे {target_chat} पर बजाना है।")

    @bot.on_message(filters.voice & filters.private)
    async def voice_handler(c, m):
        msg = await m.reply("प्ले हो रहा है...")
        file_path = await m.download()
        
        global call_py
        call_py = PyTgCalls(user_bot)
        await call_py.start()
        await call_py.join_group_call(target_chat, AudioPiped(file_path))
        await msg.edit(f"🎶 VC पर बजना शुरू हो गया!")

bot.run()

