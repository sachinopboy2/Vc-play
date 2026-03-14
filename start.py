from telegram import Update
from telegram.ext import ContextTypes
from utils.banner import START_BANNER

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_BANNER)
