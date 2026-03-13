from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

bot = Client("MasterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ऑथराइज्ड यूजर्स की लिस्ट (शुरुआत में सिर्फ आप)
SUDO_USERS = {OWNER_ID}

# --- APPROVE COMMAND ---
@bot.on_message(filters.command("approve") & filters.user(OWNER_ID))
async def approve_user(client, message):
    # 1. अगर किसी के मैसेज पर रिप्लाई करके /approve लिखा जाए
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_name = message.reply_to_message.from_user.first_name
    
    # 2. अगर /approve @username या ID लिखा जाए
    elif len(message.command) > 1:
        try:
            user_data = await client.get_users(message.command[1])
            user_id = user_data.id
            user_name = user_data.first_name
        except Exception as e:
            return await message.reply(f"❌ यूजर नहीं मिला: {e}")
    else:
        return await message.reply("सही तरीका: किसी के मैसेज पर Reply करें या `/approve @username` लिखें।")

    SUDO_USERS.add(user_id)
    await message.reply(f"✅ **{user_name}** ({user_id}) अब बोट इस्तेमाल कर सकता है!")

# --- DISAPPROVE (हटाने के लिए) ---
@bot.on_message(filters.command("disapprove") & filters.user(OWNER_ID))
async def disapprove_user(client, message):
    # (सेम लॉजिक हटाने के लिए)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_data = await client.get_users(message.command[1])
        user_id = user_data.id
    
    if user_id in SUDO_USERS:
        SUDO_USERS.remove(user_id)
        await message.reply("❌ यूजर को लिस्ट से हटा दिया गया है।")
    else:
        await message.reply("यह यूजर पहले से ही लिस्ट में नहीं है।")

# --- CHECK AUTHORIZATION ---
@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    if message.from_user.id not in SUDO_USERS:
        return await message.reply("🔒 आप इस बोट के मालिक नहीं हैं। एक्सेस के लिए ओनर से संपर्क करें।")
    
    await message.reply(f"स्वागत है मालिक! आप ऑथराइज्ड हैं।")

bot.run()

