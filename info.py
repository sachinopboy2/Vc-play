from telegram import Update
from telegram.ext import ContextTypes
from config import BOT_NAME, VERSION

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
Bot Name : {BOT_NAME}
Version  : {VERSION}
Status   : Running on VPS
"""
    await update.message.reply_text(text)
