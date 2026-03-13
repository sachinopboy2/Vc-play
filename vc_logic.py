import asyncio
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from pyrogram import Client

# यह फंक्शन VC ज्वाइन करके ऑडियो प्ले करेगा
async def join_and_play(client, chat_id, file_path):
    call_py = PyTgCalls(client)
    await call_py.start()
    
    try:
        # अगर लिंक दिया है तो ID निकालनी होगी, वरना डायरेक्ट ID यूज़ होगी
        await call_py.join_group_call(
            chat_id,
            AudioPiped(file_path)
        )
        return call_py
    except Exception as e:
        print(f"Error joining VC: {e}")
        return None
      
